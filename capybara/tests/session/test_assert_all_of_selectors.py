import pytest
import re

import capybara
from capybara.exceptions import ElementNotFound


class TestAssertAllOfSelectors:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    def test_does_not_raise_if_the_given_selectors_are_on_the_page(self, session):
        session.assert_all_of_selectors("css", "p a#foo", "h2#h2one", "h2#h2two")

    def test_raises_if_any_of_the_given_selectors_are_not_on_the_page(self, session):
        with pytest.raises(ElementNotFound):
            session.assert_all_of_selectors("css", "p a#foo", "h2#h2three", "h2#h2two")

    def test_uses_default_selector(self, session):
        capybara.default_selector = "css"
        with pytest.raises(ElementNotFound):
            session.assert_all_of_selectors("p a#foo", "h2#h2three", "h2#h2two")
        session.assert_all_of_selectors("p a#foo", "h2#h2one", "h2#h2two")

    def test_respects_scopes(self, session):
        with session.scope("//p[@id='first']"):
            session.assert_all_of_selectors(".//a[@id='foo']")
            with pytest.raises(ElementNotFound):
                session.assert_all_of_selectors(".//a[@id='red']")

    def test_applies_options_to_all_locators(self, session):
        session.assert_all_of_selectors("field", "normal", "additional_newline", field_type="textarea")
        with pytest.raises(ElementNotFound):
            session.assert_all_of_selectors("field", "normal", "test_field", "additional_newline", field_type="textarea")

    @pytest.mark.requires("js")
    def test_does_not_raise_error_if_all_the_elements_appear_before_given_wait_duration(self, session):
        with capybara.using_wait_time(0.1):
            session.visit("/with_js")
            session.click_link("Click me")
            session.assert_all_of_selectors("css", "a#clickable", "a#has-been-clicked", "#drag", wait=0.9)


class TestAssertNoneOfSelectors:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    def test_raises_if_any_of_the_given_selectors_are_on_the_page(self, session):
        with pytest.raises(ElementNotFound):
            session.assert_none_of_selectors("xpath", "//p", "//a")
        with pytest.raises(ElementNotFound):
            session.assert_none_of_selectors("xpath", "//abbr", "//a")
        with pytest.raises(ElementNotFound):
            session.assert_none_of_selectors("css", "p a#foo")

    def test_does_not_raise_if_any_of_the_given_selectors_are_not_on_the_page(self, session):
        session.assert_none_of_selectors("xpath", "//abbr", "//td")
        session.assert_none_of_selectors("css", "p a#doesnotexist", "abbr")

    def test_uses_default_selector(self, session):
        capybara.default_selector = "css"
        session.assert_none_of_selectors("css", "p a#doesnotexist", "abbr")
        with pytest.raises(ElementNotFound):
            session.assert_none_of_selectors("abbr", "p a#foo")

    def test_respects_scopes(self, session):
        with session.scope("//p[@id='first']"):
            with pytest.raises(ElementNotFound):
                session.assert_none_of_selectors(".//a[@id='foo']")
            session.assert_none_of_selectors(".//a[@id='red']")

    def test_applies_the_options_to_all_locators(self, session):
        with pytest.raises(ElementNotFound):
            session.assert_none_of_selectors("//p//a", text="Redirect")
        session.assert_none_of_selectors("//p", text="Doesnotexist")

    def test_discards_all_matches_where_the_given_regexp_is_matched(self, session):
        with pytest.raises(ElementNotFound):
            session.assert_none_of_selectors("//p//a", text=re.compile(r"re[dab]i", re.IGNORECASE), count=1)
        session.assert_none_of_selectors("//p//a", text=re.compile(r"Red$"))

    @pytest.mark.requires("js")
    def test_does_not_find_elements_if_they_appear_after_given_wait_duration(self, session):
        with capybara.using_wait_time(0.1):
            session.visit("/with_js")
            session.click_link("Click me")
            session.assert_none_of_selectors("css", "#new_field", "a#has-been-clicked", wait=0.1)
