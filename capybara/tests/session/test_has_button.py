import pytest


class TestHasButton:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/form")

    def test_is_true_if_the_given_button_is_on_the_page(self, session):
        assert session.has_button("med")
        assert session.has_button("crap321")

    def test_is_false_if_the_given_button_is_not_on_the_page(self, session):
        assert not session.has_button("monkey")
