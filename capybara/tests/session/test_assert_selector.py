import pytest
import re

import capybara
from capybara.exceptions import ElementNotFound


class TestAssertSelector:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    def test_does_not_raise_if_the_given_selector_is_on_the_page(self, session):
        session.assert_selector("xpath", "//p")
        session.assert_selector("css", "p a#foo")
        session.assert_selector("//p[contains(.,'est')]")

    def test_raises_if_the_given_selector_is_not_on_the_page(self, session):
        with pytest.raises(ElementNotFound):
            session.assert_selector("xpath", "//abbr")
        with pytest.raises(ElementNotFound):
            session.assert_selector("css", "p a#doesnotexist")
        with pytest.raises(ElementNotFound):
            session.assert_selector("//p[contains(.,'thisstringisnotonpage')]")

    def test_uses_default_selector(self, session):
        capybara.default_selector = "css"
        with pytest.raises(ElementNotFound):
            session.assert_selector("p a#doesnotexist")
        session.assert_selector("p a#foo")

    def test_respects_scopes(self, session):
        with session.scope("//p[@id='first']"):
            session.assert_selector(".//a[@id='foo']")
            with pytest.raises(ElementNotFound):
                session.assert_selector(".//a[@id='red']")

    def test_is_true_if_the_content_is_on_the_page_the_given_number_of_times(self, session):
        session.assert_selector("//p", count=3)
        session.assert_selector("//p//a[@id='foo']", count=1)
        session.assert_selector("//p[contains(.,'est')]", count=1)

    def test_raises_if_the_content_is_on_the_page_the_given_number_of_times(self, session):
        with pytest.raises(ElementNotFound):
            session.assert_selector("//p", count=6)
        with pytest.raises(ElementNotFound):
            session.assert_selector("//p//a[@id='foo']", count=2)
        with pytest.raises(ElementNotFound):
            session.assert_selector("//p[contains(.,'est')]", count=5)

    def test_raises_if_the_content_is_not_on_the_page_at_all(self, session):
        with pytest.raises(ElementNotFound):
            session.assert_selector("//abbr", count=2)
        with pytest.raises(ElementNotFound):
            session.assert_selector("//p//a[@id='doesnotexist']", count=1)

    def test_discards_all_matches_where_the_given_string_is_not_contained(self, session):
        session.assert_selector("//p//a", text="Redirect", count=1)
        with pytest.raises(ElementNotFound):
            session.assert_selector("//p", text="Doesnotexist")

    def test_discards_all_matches_where_the_given_regex_is_not_matched(self, session):
        session.assert_selector("//p//a", text=re.compile("re[dab]i", re.IGNORECASE), count=1)
        with pytest.raises(ElementNotFound):
            session.assert_selector("//p//a", text=re.compile("Red$"))

    @pytest.mark.requires("js")
    def test_finds_element_if_it_appears_before_given_wait_duration(self, session):
        with capybara.using_wait_time(0.1):
            session.visit("/with_js")
            session.click_link("Click me")
            session.assert_selector("css", "a#has-been-clicked", text="Has been clicked", wait=0.9)


class TestAssertNoSelector:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    def test_raises_an_error_if_the_given_selector_is_on_the_page(self, session):
        with pytest.raises(ElementNotFound):
            session.assert_no_selector("xpath", "//p")
        with pytest.raises(ElementNotFound):
            session.assert_no_selector("css", "p a#foo")
        with pytest.raises(ElementNotFound):
            session.assert_no_selector("//p[contains(.,'est')]")

    def test_is_true_if_the_given_selector_is_not_on_the_page(self, session):
        session.assert_no_selector("xpath", "//abbr")
        session.assert_no_selector("css", "p a#doesnotexist")
        session.assert_no_selector("//p[contains(.,'thisstringisnotonpage')]")

    def test_uses_the_default_selector(self, session):
        capybara.default_selector = "css"
        session.assert_no_selector("p a#doesnotexist")
        with pytest.raises(ElementNotFound):
            session.assert_no_selector("p a#foo")

    def test_respects_scopes(self, session):
        with session.scope("//p[@id='first']"):
            with pytest.raises(ElementNotFound):
                session.assert_no_selector(".//a[@id='foo']")
            session.assert_no_selector(".//a[@id='red']")

    def test_raises_an_error_if_the_content_is_on_the_page_the_given_number_of_times(self, session):
        with pytest.raises(ElementNotFound):
            session.assert_no_selector("//p", count=3)
        with pytest.raises(ElementNotFound):
            session.assert_no_selector("//p//a[@id='foo']", count=1)
        with pytest.raises(ElementNotFound):
            session.assert_no_selector("//p[contains(.,'est')]", count=1)

    def test_is_true_if_the_content_is_on_the_page_the_wrong_number_of_times(self, session):
        session.assert_no_selector("//p", count=6)
        session.assert_no_selector("//p//a[@id='foo']", count=2)
        session.assert_no_selector("//p[contains(.,'est')]", count=5)

    def test_is_true_if_the_content_is_not_on_the_page_at_all(self, session):
        session.assert_no_selector("//abbr", count=2)
        session.assert_no_selector("//p//a[@id='doesnotexist']", count=1)

    def test_discards_all_matches_where_the_given_string_is_contained(self, session):
        with pytest.raises(ElementNotFound):
            session.assert_no_selector("//p//a", text="Redirect", count=1)
        session.assert_no_selector("//p", text="Doesnotexist")

    def test_discards_all_matches_where_the_given_regex_is_matched(self, session):
        with pytest.raises(ElementNotFound):
            session.assert_no_selector("//p//a", text=re.compile(r"re[dab]i", re.IGNORECASE), count=1)
        session.assert_no_selector("//p//a", text=re.compile(r"Red$"))

    @pytest.mark.requires("js")
    def test_does_not_find_element_if_it_appears_after_given_wait_duration(self, session):
        session.visit("/with_js")
        session.click_link("Click me")
        session.assert_no_selector("css", "a#has-been-clicked", text="Has been clicked", wait=0.1)
