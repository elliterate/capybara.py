import pytest

from capybara.exceptions import ElementNotFound
from capybara.tests.helpers import extract_results


class ChooseTestCase:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/form")


class TestChoose(ChooseTestCase):
    def test_chooses_a_radio_button_by_id(self, session):
        session.choose("gender_male")
        session.click_button("awesome")
        assert extract_results(session)["form[gender]"] == "male"

    def test_chooses_a_radio_button_by_label(self, session):
        session.choose("Both")
        session.click_button("awesome")
        assert extract_results(session)["form[gender]"] == "both"

    def test_chooses_an_approximately_matching_radio_button(self, session):
        session.choose("Mal")
        session.click_button("awesome")
        assert extract_results(session)["form[gender]"] == "male"

    def test_raises_an_error_with_a_locator_that_does_not_exist(self, session):
        with pytest.raises(ElementNotFound):
            session.choose("does not exist")


class TestExactChoose(ChooseTestCase):
    def test_raises_an_error_for_an_approximately_matching_radio_button(self, session):
        with pytest.raises(ElementNotFound):
            session.choose("Mal", exact=True)
