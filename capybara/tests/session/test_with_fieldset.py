import pytest

from capybara.tests.helpers import extract_results


class TestWithFieldset:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/fieldsets")

    def test_restricts_scope_to_a_fieldset_given_by_id(self, session):
        with session.fieldset("villain_fieldset"):
            session.fill_in("Name", value="Goldfinger")
            session.click_button("Create")
        assert extract_results(session)["form[villain_name]"] == "Goldfinger"

    def test_restricts_scope_to_a_fieldset_given_by_legend(self, session):
        with session.fieldset("Villain"):
            session.fill_in("Name", value="Goldfinger")
            session.click_button("Create")
        assert extract_results(session)["form[villain_name]"] == "Goldfinger"
