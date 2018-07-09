import pytest
import re


@pytest.mark.requires("css")
class TestHasStyle:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    def test_is_true_if_the_element_has_the_given_style(self, session):
        assert session.find("css", "#first").has_style({"display": "block"}) is True
        assert session.find("css", "#second").has_style({"display": "inline"}) is True

    def test_is_false_if_the_element_does_not_have_the_given_style(self, session):
        assert session.find("css", "#first").has_style({"display": "inline"}) is False
        assert session.find("css", "#second").has_style({"display": "block"}) is False

    def test_allows_regexp_for_value_matching(self, session):
        assert session.find("css", "#first").has_style({"display": re.compile(r"^bl")}) is True
        assert session.find("css", "#first").has_style({"display": re.compile(r"^in")}) is False
