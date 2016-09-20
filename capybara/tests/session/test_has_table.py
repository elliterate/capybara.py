import pytest


class TestHasTable:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/tables")

    def test_is_true_if_the_table_is_on_the_page(self, session):
        assert session.has_table("Villain")
        assert session.has_table("villain_table")

    def test_is_false_if_the_table_is_not_on_the_page(self, session):
        assert not session.has_table("Monkey")


class TestHasNoTable:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/tables")

    def test_is_false_if_the_table_is_on_the_page(self, session):
        assert not session.has_no_table("Villain")
        assert not session.has_no_table("villain_table")

    def test_is_true_if_the_table_is_not_on_the_page(self, session):
        assert session.has_no_table("Monkey")
