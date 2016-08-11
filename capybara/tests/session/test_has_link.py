import pytest


class TestHasLink:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    def test_is_true_if_the_given_link_is_on_the_page(self, session):
        assert session.has_link("foo")
        assert session.has_link("awesome title")

    def test_is_false_if_the_given_link_is_not_on_the_page(self, session):
        assert not session.has_link("monkey")
