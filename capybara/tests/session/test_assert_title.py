import pytest

from capybara.exceptions import ExpectationNotMet


class TestAssertTitle:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_js")

    def test_is_true_if_the_page_title_contains_the_given_string(self, session):
        assert session.assert_title("js") is True

    def test_is_true_when_given_an_empty_string(self, session):
        assert session.assert_title("") is True

    def test_waits_for_title(self, session):
        session.click_link("Change title")
        assert session.assert_title("changed title") is True

    def test_raises_error_if_the_page_title_does_not_contain_the_given_string(self, session):
        with pytest.raises(ExpectationNotMet) as excinfo:
            session.assert_title("monkey")
        assert "expected 'with_js' to include 'monkey'" in str(excinfo.value)

    def test_normalizes_the_given_title(self, session):
        session.assert_title("  with_js  ")

    def test_normalizes_given_title_in_error_message(self, session):
        with pytest.raises(ExpectationNotMet) as excinfo:
            session.assert_title(2)
        assert "expected 'with_js' to include '2'" in str(excinfo.value)
