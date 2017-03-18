import pytest
import re

from capybara.exceptions import ExpectationNotMet


class TestAssertCurrentPath:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_js")

    def test_does_not_raise_if_the_page_has_the_given_current_path(self, session):
        session.assert_current_path("/with_js")

    def test_allows_regexp_matches(self, session):
        session.assert_current_path(re.compile(r"w[a-z]{3}_js"))

    def test_handles_non_escaped_query_options(self, session):
        session.click_link("Non-escaped query options")
        session.assert_current_path("/with_html?options[]=things")

    def test_handles_escaped_query_options(self, session):
        session.click_link("Escaped query options")
        session.assert_current_path("/with_html?options%5B%5D=things")

    @pytest.mark.requires("js")
    def test_waits_for_current_path(self, session):
        session.click_link("Change page")
        session.assert_current_path("/with_html")

    def test_raises_an_error_if_the_page_does_not_have_the_given_current_path(self, session):
        with pytest.raises(ExpectationNotMet) as excinfo:
            session.assert_current_path("/with_html")
        assert "expected '/with_js' to equal '/with_html'" in str(excinfo.value)

    def test_checks_query_options(self, session):
        session.visit("/with_js?test=test")
        session.assert_current_path("/with_js?test=test")

    def test_compares_the_full_url(self, session):
        session.assert_current_path(re.compile(r"\Ahttp://[^/]*/with_js\Z"), url=True)

    def test_ignores_the_query(self, session):
        session.visit("/with_js?test=test")
        session.assert_current_path("/with_js?test=test")
        session.assert_current_path("/with_js", only_path=True)


class TestAssertNoCurrentPath:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_js")

    def test_raises_if_the_page_has_the_given_current_path(self, session):
        with pytest.raises(ExpectationNotMet):
            session.assert_no_current_path("/with_js")

    def test_allows_regex_matches(self, session):
        session.assert_no_current_path(re.compile(r"monkey"))

    @pytest.mark.requires("js")
    def test_waits_for_current_path_to_disappear(self, session):
        session.click_link("Change page")
        session.assert_no_current_path("/with_js")

    def test_does_not_raise_if_the_page_does_not_have_the_given_current_path(self, session):
        session.assert_no_current_path("/with_html")
