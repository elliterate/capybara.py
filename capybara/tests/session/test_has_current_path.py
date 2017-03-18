import pytest
import re


class TestHasCurrentPath:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_js")

    def test_is_true_if_the_page_has_the_given_current_path(self, session):
        assert session.has_current_path("/with_js")

    def test_allows_regexp_matches(self, session):
        assert session.has_current_path(re.compile(r"w[a-z]{3}_js"))
        assert not session.has_current_path(re.compile(r"monkey"))

    def test_handles_non_escaped_query_options(self, session):
        session.click_link("Non-escaped query options")
        assert session.has_current_path("/with_html?options[]=things")

    def test_handles_escaped_query_options(self, session):
        session.click_link("Escaped query options")
        assert session.has_current_path("/with_html?options%5B%5D=things")

    @pytest.mark.requires("js")
    def test_waits_for_current_path(self, session):
        session.click_link("Change page")
        assert session.has_current_path("/with_html")

    def test_is_false_if_the_page_does_not_have_the_given_current_path(self, session):
        assert not session.has_current_path("/with_html")

    def test_checks_query_options(self, session):
        session.visit("/with_js?test=test")
        assert session.has_current_path("/with_js?test=test")

    def test_compares_the_full_url(self, session):
        assert session.has_current_path(re.compile(r"\Ahttp://[^/]*/with_js\Z"), url=True)

    def test_ignores_the_query(self, session):
        session.visit("/with_js?test=test")
        assert session.has_current_path("/with_js?test=test")
        assert session.has_current_path("/with_js", only_path=True)

    def test_does_not_allow_url_and_only_path_at_the_same_time(self, session):
        with pytest.raises(RuntimeError):
            session.has_current_path("/with_js", url=True, only_path=True)


class TestHasNoCurrentPath:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_js")

    def test_is_false_if_the_page_has_the_given_current_path(self, session):
        assert not session.has_no_current_path("/with_js")

    def test_allows_regex_matches(self, session):
        assert not session.has_no_current_path(re.compile(r"w[a-z]{3}_js"))
        assert session.has_no_current_path(re.compile(r"monkey"))

    @pytest.mark.requires("js")
    def test_waits_for_current_path_to_disappear(self, session):
        session.click_link("Change page")
        assert session.has_no_current_path("/with_js")

    def test_is_true_if_the_page_does_not_have_the_given_current_path(self, session):
        assert session.has_no_current_path("/with_html")
