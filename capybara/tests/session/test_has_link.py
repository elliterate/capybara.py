import pytest
import re


class TestHasLink:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    def test_is_true_if_the_given_link_is_on_the_page(self, session):
        assert session.has_link("foo")
        assert session.has_link("awesome title")
        assert session.has_link("A link", href="/with_simple_html")
        assert session.has_link("A link", href=re.compile(r"\/with_simple_html"))

    def test_is_false_if_the_given_link_is_not_on_the_page(self, session):
        assert not session.has_link("monkey")
        assert not session.has_link("A link", href="/non-existant-href")
        assert not session.has_link("A link", href=re.compile(r"non-existant"))


class TestHasNoLink:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    def test_is_false_if_the_given_link_is_on_the_page(self, session):
        assert not session.has_no_link("foo")
        assert not session.has_no_link("awesome title")
        assert not session.has_no_link("A link", href="/with_simple_html")
        assert not session.has_no_link("A link", href=re.compile(r"\/with_simple_html"))

    def test_is_true_if_the_given_link_is_not_on_the_page(self, session):
        assert session.has_no_link("monkey")
        assert session.has_no_link("A link", href="/non-existant-href")
        assert session.has_no_link("A link", href=re.compile(r"non-existant"))
