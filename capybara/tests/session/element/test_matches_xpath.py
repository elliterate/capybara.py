import pytest

import capybara


class MatchesXPathTestCase:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    @pytest.fixture
    def element(self, session):
        return session.find("css", "span", text="42")


class TestMatchesXPath(MatchesXPathTestCase):
    def test_is_true_if_the_given_selector_matches_the_element(self, element):
        assert element.matches_xpath("//span")
        assert element.matches_xpath("//span[@class='number']")

    def test_is_false_if_the_given_selector_does_not_match(self, element):
        assert not element.matches_xpath("//abbr")
        assert not element.matches_xpath("//div")
        assert not element.matches_xpath("//span[@class='not_a_number']")

    def test_uses_xpath_even_if_default_selector_is_css(self, element):
        capybara.default_selector = "css"
        assert not element.matches_xpath("//span[@class='not_a_number']")
        assert not element.matches_xpath("//div[@class='number']")


class TestNotMatchXPath(MatchesXPathTestCase):
    def test_is_false_if_the_given_selector_matches_the_element(self, element):
        assert not element.not_match_xpath("//span")
        assert not element.not_match_xpath("//span[@class='number']")

    def test_is_true_if_the_given_selector_does_not_match(self, element):
        assert element.not_match_xpath("//abbr")
        assert element.not_match_xpath("//div")
        assert element.not_match_xpath("//span[@class='not_a_number']")

    def test_uses_xpath_even_if_default_selector_is_css(self, element):
        capybara.default_selector = "css"
        assert element.not_match_xpath("//span[@class='not_a_number']")
        assert element.not_match_xpath("//div[@class='number']")
