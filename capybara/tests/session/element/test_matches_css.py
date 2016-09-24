import pytest


class MatchesCSSTestCase:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    @pytest.fixture
    def element(self, session):
        return session.find("css", "span", text="42")


class TestMatchesCSS(MatchesCSSTestCase):
    def test_is_true_if_the_given_selector_matches_the_element(self, element):
        assert element.matches_css("span")
        assert element.matches_css("span.number")

    def test_is_false_if_the_given_selector_does_not_match(self, element):
        assert not element.matches_css("div")
        assert not element.matches_css("p a#doesnotexist")
        assert not element.matches_css("p.nosuchclass")


class TestNotMatchCSS(MatchesCSSTestCase):
    def test_is_false_if_the_given_selector_matches_the_element(self, element):
        assert not element.not_match_css("span")
        assert not element.not_match_css("span.number")

    def test_is_true_if_the_given_selector_does_not_match(self, element):
        assert element.not_match_css("div")
        assert element.not_match_css("p a#doesnotexist")
        assert element.not_match_css("p.nosuchclass")
