import pytest


class TestHasTitle:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_js")

    def test_is_true_if_the_page_has_the_given_title(self, session):
        assert session.has_title("with_js")

    def test_waits_for_title(self, session):
        session.click_link("Change title")
        assert session.has_title("changed title")

    def test_is_false_if_the_page_does_not_have_the_given_title(self, session):
        assert not session.has_title("monkey")
