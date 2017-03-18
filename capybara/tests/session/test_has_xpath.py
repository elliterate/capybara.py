import pytest
import re

import capybara


class TestHasXPath:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    def test_is_true_if_the_given_selector_is_on_the_page(self, session):
        assert session.has_xpath("//p")
        assert session.has_xpath("//p//a[@id='foo']")
        assert session.has_xpath("//p[contains(.,'est')]")

    def test_is_false_if_the_given_selector_is_not_on_the_page(self, session):
        assert not session.has_xpath("//abbr")
        assert not session.has_xpath("//p//a[@id='doesnotexist']")
        assert not session.has_xpath("//p[contains(.,'thisstringisnotonpage')]")

    def test_uses_xpath_even_if_default_selector_is_css(self, session):
        capybara.default_selector = "css"
        assert not session.has_xpath("//p//a[@id='doesnotexist']")

    def test_respects_scopes(self, session):
        with session.scope("//p[@id='first']"):
            assert session.has_xpath(".//a[@id='foo']")
            assert not session.has_xpath(".//a[@id='red']")

    @pytest.mark.requires("js")
    def test_waits_for_content_to_appear(self, session):
        session.visit("/with_js")
        session.click_link("Click me")
        assert session.has_xpath("//input[@type='submit' and @value='New Here']")

    def test_is_true_if_the_content_occurs_the_given_number_of_times(self, session):
        assert session.has_xpath("//p", count=3)
        assert session.has_xpath("//p//a[@id='foo']", count=1)
        assert session.has_xpath("//p[contains(.,'est')]", count=1)
        assert session.has_xpath("//p//a[@id='doesnotexist']", count=0)

    def test_is_false_if_the_content_occurs_a_different_number_of_times_than_the_given(self, session):
        assert not session.has_xpath("//p", count=6)
        assert not session.has_xpath("//p//a[@id='foo']", count=2)
        assert not session.has_xpath("//p[contains(.,'est')]", count=5)
        assert not session.has_xpath("//p//a[@id='doesnotexist']", count=1)

    def test_discards_all_matches_where_the_given_string_is_not_contained(self, session):
        assert session.has_xpath("//p//a", text="Redirect", count=1)
        assert not session.has_xpath("//p", text="Doesnotexist")

    def test_discards_all_matches_where_the_given_regex_is_not_matched(self, session):
        assert session.has_xpath("//p//a", text=re.compile("re[dab]i", re.IGNORECASE), count=1)
        assert not session.has_xpath("//p", text=re.compile("Red$"))


class TestHasNoXPath:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    def test_is_false_if_the_given_selector_is_on_the_page(self, session):
        assert not session.has_no_xpath("//p")
        assert not session.has_no_xpath("//p//a[@id='foo']")
        assert not session.has_no_xpath("//p[contains(.,'est')]")

    def test_is_true_if_the_given_selector_is_not_on_the_page(self, session):
        assert session.has_no_xpath("//abbr")
        assert session.has_no_xpath("//p//a[@id='doesnotexist']")
        assert session.has_no_xpath("//p[contains(.,'thisstringisnotonpage')]")

    def test_uses_xpath_even_if_default_selector_is_css(self, session):
        capybara.default_selector = "css"
        assert session.has_no_xpath("//p//a[@id='doesnotexist']")

    def test_respects_scopes(self, session):
        with session.scope("//p[@id='first']"):
            assert not session.has_no_xpath(".//a[@id='foo']")
            assert session.has_no_xpath(".//a[@id='red']")

    @pytest.mark.requires("js")
    def test_waits_for_content_to_disappear(self, session):
        session.visit("/with_js")
        session.click_link("Click me")
        assert session.has_no_xpath("//p[@id='change']")

    def test_is_false_if_the_content_occurs_the_given_number_of_times(self, session):
        assert not session.has_no_xpath("//p", count=3)
        assert not session.has_no_xpath("//p//a[@id='foo']", count=1)
        assert not session.has_no_xpath("//p[contains(.,'est')]", count=1)
        assert not session.has_no_xpath("//p//a[@id='doesnotexist']", count=0)

    def test_is_true_if_the_content_occurs_a_different_number_of_times_than_the_given(self, session):
        assert session.has_no_xpath("//p", count=6)
        assert session.has_no_xpath("//p//a[@id='foo']", count=2)
        assert session.has_no_xpath("//p[contains(.,'est')]", count=5)
        assert session.has_no_xpath("//p//a[@id='doesnotexist']", count=1)

    def test_discards_all_matches_where_the_given_string_is_contained(self, session):
        assert not session.has_no_xpath("//p//a", text="Redirect", count=1)
        assert session.has_no_xpath("//p", text="Doesnotexist")

    def test_discards_all_matches_where_the_given_regex_is_matched(self, session):
        assert not session.has_no_xpath("//p//a", text=re.compile("re[dab]i", re.IGNORECASE), count=1)
        assert session.has_no_xpath("//p", text=re.compile("Red$"))
