import pytest
import re

import capybara


class TestHaveNoneOfSelectors:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    def test_is_false_if_any_of_the_given_locators_are_on_the_page(self, session):
        assert session.has_none_of_selectors("xpath", "//p", "//a") is False
        assert session.has_none_of_selectors("css", "p a#foo") is False

    def test_is_true_if_none_of_the_given_locators_are_on_the_page(self, session):
        assert session.has_none_of_selectors("xpath", "//abbr", "//td") is True
        assert session.has_none_of_selectors("css", "p a#doesnotexist", "abbr") is True

    def test_uses_default_selector(self, session):
        capybara.default_selector = "css"
        assert session.has_none_of_selectors("p a#doesnotexist", "abbr")
        assert not session.has_none_of_selectors("abbr", "p a#foo")

    def test_respects_scopes_when_used_with_a_context(self, session):
        with session.scope("//p[@id='first']"):
            assert not session.has_none_of_selectors(".//a[@id='foo']")
            assert session.has_none_of_selectors(".//a[@id='red']")

    def test_respects_scopes_when_called_on_an_element(self, session):
        el = session.find("//p[@id='first']")
        assert not el.has_none_of_selectors(".//a[@id='foo']")
        assert el.has_none_of_selectors(".//a[@id='red']")

    def test_applies_the_options_to_all_locators(self, session):
        assert not session.has_none_of_selectors("//p//a", text="Redirect")
        assert session.has_none_of_selectors("//p", text="Doesnotexist")

    def test_discards_all_matches_where_the_given_regexp_is_matched(self, session):
        assert not session.has_none_of_selectors(
            "//p//a", text=re.compile(r"re[dab]i", re.IGNORECASE), count=1)
        assert session.has_none_of_selectors("//p//a", text=re.compile(r"Red$"))

    @pytest.mark.requires("js")
    def test_does_not_find_elements_if_they_appear_after_given_wait_duration(self, session):
        session.visit("/with_js")
        session.click_link("Click me")
        assert session.has_none_of_selectors("css", "#new_field", "a#has-been-clicked", wait=0.1)
