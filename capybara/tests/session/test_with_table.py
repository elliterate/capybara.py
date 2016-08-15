import pytest

from capybara.tests.helpers import extract_results


class TestWithTable:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/tables")

    def test_restricts_scope_to_a_table_given_by_id(self, session):
        with session.table("girl_table"):
            session.fill_in("Name", value="Christmas")
            session.click_button("Create")
        assert extract_results(session)["form[girl_name]"] == "Christmas"

    def test_restricts_scope_to_a_table_given_by_caption(self, session):
        with session.table("Villain"):
            session.fill_in("Name", value="Quantum")
            session.click_button("Create")
        assert extract_results(session)["form[villain_name]"] == "Quantum"
