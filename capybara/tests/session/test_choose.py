import pytest

import capybara
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

    def test_raises_an_error_for_a_disabled_radio_button(self, session):
        with pytest.raises(ElementNotFound):
            session.choose("Disabled Radio")


class TestExactChoose(ChooseTestCase):
    def test_raises_an_error_for_an_approximately_matching_radio_button(self, session):
        with pytest.raises(ElementNotFound):
            session.choose("Mal", exact=True)


class TestChooseWithAutomaticLabelClick(ChooseTestCase):
    @pytest.fixture(autouse=True)
    def setup_settings(self):
        old_automatic_label_click = capybara.automatic_label_click
        capybara.automatic_label_click = True
        try:
            yield
        finally:
            capybara.automatic_label_click = old_automatic_label_click

    def test_selects_by_clicking_the_link_if_available(self, session):
        session.choose("party_democrat")
        session.click_button("awesome")
        assert extract_results(session)["form[party]"] == "democrat"

    def test_raises_an_error_if_not_allowed_to_click_label(self, session):
        with pytest.raises(ElementNotFound) as excinfo:
            session.choose("party_democrat", allow_label_click=False)
        assert "Unable to find radio button 'party_democrat'" in str(excinfo.value)
