import pytest
import re

from capybara.exceptions import ExpectationNotMet


class TestAssertTitle:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_js")

    def test_is_true_if_the_page_title_contains_the_given_string(self, session):
        assert session.assert_title("js") is True

    def test_is_true_when_given_an_empty_string(self, session):
        assert session.assert_title("") is True

    def test_allows_regex_matches(self, session):
        assert session.assert_title(re.compile(r"w[a-z]{3}_js")) is True
        with pytest.raises(ExpectationNotMet) as excinfo:
            session.assert_title(re.compile(r"w[a-z]{10}_js"))
        assert "expected 'with_js' to match 'w[a-z]{10}_js'" in str(excinfo.value)

    @pytest.mark.requires("js")
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


class TestAssertNoTitle:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_js")

    def test_raises_error_if_the_title_contains_the_given_string(self, session):
        with pytest.raises(ExpectationNotMet) as excinfo:
            session.assert_no_title("with_j")
        assert "expected 'with_js' not to include 'with_j'" in str(excinfo.value)

    def test_allows_regex_matches(self, session):
        with pytest.raises(ExpectationNotMet) as excinfo:
            session.assert_no_title(re.compile(r"w[a-z]{3}_js"))
        assert "expected 'with_js' not to match 'w[a-z]{3}_js'" in str(excinfo.value)
        session.assert_no_title(re.compile(r"monkey"))

    @pytest.mark.requires("js")
    def test_waits_for_title_to_disappear(self, session):
        session.click_link("Change title")
        assert session.assert_no_title("with_js") is True

    def test_is_true_if_the_title_does_not_contain_the_string(self, session):
        assert session.assert_no_title("monkey") is True
