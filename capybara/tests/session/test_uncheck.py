import pytest

import capybara
from capybara.exceptions import ElementNotFound
from capybara.tests.helpers import extract_results


class UncheckTestCase:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/form")


class TestUncheck(UncheckTestCase):
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


class TestUncheckWithAutomaticLabelClick(UncheckTestCase):
    @pytest.fixture(autouse=True)
    def setup_settings(self):
        old_automatic_label_click = capybara.automatic_label_click
        capybara.automatic_label_click = True
        try:
            yield
        finally:
            capybara.automatic_label_click = old_automatic_label_click

    def test_unchecks_via_clicking_the_label_with_for_attribute_if_possible(self, session):
        assert session.find("checkbox", "form_cars_jaguar", checked=True, visible="hidden")
        session.uncheck("form_cars_jaguar")
        session.click_button("awesome")
        assert "jaguar" not in extract_results(session).getlist("form[cars][]")

    def test_unchecks_via_clicking_the_wrapping_label_if_possible(self, session):
        assert session.find("checkbox", "form_cars_koenigsegg", checked=True, visible="hidden")
        session.uncheck("form_cars_koenigsegg")
        session.click_button("awesome")
        assert "koenigsegg" not in extract_results(session).getlist("form[cars][]")

    def test_does_not_click_the_label_if_unneeded(self, session):
        assert session.find("checkbox", "form_cars_tesla", unchecked=True, visible="hidden")
        session.uncheck("form_cars_tesla")
        session.click_button("awesome")
        assert "tesla" not in extract_results(session).getlist("form[cars][]")

    def test_raises_original_error_when_no_label_available(self, session):
        with pytest.raises(ElementNotFound) as excinfo:
            session.uncheck("form_cars_ariel")
        assert "Unable to find checkbox 'form_cars_ariel'" in str(excinfo.value)

    def test_raises_error_if_not_allowed_to_click_label(self, session):
        with pytest.raises(ElementNotFound) as excinfo:
            session.uncheck("form_cars_jaguar", allow_label_click=False)
        assert "Unable to find checkbox 'form_cars_jaguar'" in str(excinfo.value)
