import pytest

import capybara


class MatchesSelectorTestCase:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    @pytest.fixture
    def element(self, session):
        return session.find("//span", text="42")


class TestMatchesSelector(MatchesSelectorTestCase):
    def test_is_true_if_the_element_matches_the_given_selector(self, element):
        assert element.matches_selector("xpath", "//span") is True
        assert element.matches_selector("css", "span.number") is True

    def test_is_false_if_the_element_does_not_match_the_given_selector(self, element):
        assert element.matches_selector("xpath", "//div") is False
        assert element.matches_selector("css", "span.not_a_number") is False

    def test_uses_default_selector(self, element):
        capybara.default_selector = "css"
        assert not element.matches_selector("span.not_a_number")
        assert element.matches_selector("span.number")

    def test_discards_all_matches_where_the_given_string_is_not_contained(self, element):
        assert element.matches_selector("//span", text="42")
        assert not element.matches_selector("//span", text="Doesnotexist")


class TestNotMatchSelector(MatchesSelectorTestCase):
    def test_is_false_if_the_element_matches_the_given_selector(self, element):
        assert element.not_match_selector("xpath", "//span") is False
        assert element.not_match_selector("css", "span.number") is False

    def test_is_true_if_the_element_does_not_match_the_given_selector(self, element):
        assert element.not_match_selector("xpath", "//div") is True
        assert element.not_match_selector("css", "span.not_a_number") is True

    def test_uses_default_selector(self, element):
        capybara.default_selector = "css"
        assert element.not_match_selector("span.not_a_number")
        assert not element.not_match_selector("span.number")

    def test_discards_all_matches_where_the_given_string_is_contained(self, element):
        assert not element.not_match_selector("//span", text="42")
        assert element.not_match_selector("//span", text="Doesnotexist")
