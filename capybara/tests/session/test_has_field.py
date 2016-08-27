import pytest


class TestHasField:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/form")

    def test_is_true_if_the_field_is_on_the_page(self, session):
        assert session.has_field("Dog")
        assert session.has_field("form_description")
        assert session.has_field("Region")

    def test_is_false_if_the_field_is_not_on_the_page(self, session):
        assert not session.has_field("Monkey")
