import pytest

from capybara.exceptions import ElementNotFound


class AssertMatchesSelectorTestCase:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    @pytest.fixture
    def element(self, session):
        return session.find("css", "span", text="42")


class TestAssertMatchesSelector(AssertMatchesSelectorTestCase):
    def test_is_true_if_the_given_selector_matches_the_element(self, element):
        assert element.assert_matches_selector("css", ".number") is True

    def test_raises_error_if_the_given_selector_does_not_match_the_element(self, element):
        with pytest.raises(ElementNotFound):
            element.assert_matches_selector("css", ".not_number")

    @pytest.mark.requires("js")
    def test_waits_for_match_to_occur(self, session):
        session.visit("/with_js")
        field = session.find("css", "#disable-on-click")

        assert field.assert_matches_selector("css", "input:enabled") is True
        field.click()
        assert field.assert_matches_selector("css", "input:disabled") is True


class TestAssertNotMatchSelector(AssertMatchesSelectorTestCase):
    def test_raises_error_if_the_given_selector_matches_the_element(self, element):
        with pytest.raises(ElementNotFound):
            element.assert_not_match_selector("css", ".number")

    def test_is_true_if_the_given_selector_does_not_match_the_element(self, element):
        assert element.assert_not_match_selector("css", ".not_number") is True

    @pytest.mark.requires("js")
    def test_waits_for_match_to_fail(self, session):
        session.visit("/with_js")
        field = session.find("css", "#disable-on-click")

        assert field.assert_not_match_selector("css", "input:disabled") is True
        field.click()
        assert field.assert_not_match_selector("css", "input:enabled") is True
