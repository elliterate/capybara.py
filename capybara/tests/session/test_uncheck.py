import pytest

from capybara.tests.helpers import extract_results


class TestUncheck:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/form")

    def test_unchecks_a_checkbox_by_id(self, session):
        session.uncheck("form_pets_hamster")
        session.click_button("awesome")
        pets = extract_results(session).getlist("form[pets][]")
        assert "dog" in pets
        assert "hamster" not in pets

    def test_unchecks_a_checkbox_by_label(self, session):
        session.uncheck("Hamster")
        session.click_button("awesome")
        pets = extract_results(session).getlist("form[pets][]")
        assert "dog" in pets
        assert "hamster" not in pets
