import pytest

import capybara
from capybara.exceptions import ElementNotFound
from capybara.tests.helpers import extract_results


class CheckTestCase:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/form")


class TestCheck(CheckTestCase):
    def test_checked_attribute_s_true_if_checked(self, session):
        session.check("Terms of Use")
        assert session.find("xpath", "//input[@id='form_terms_of_use']").checked

    def test_checked_attribute_is_false_if_unchecked(self, session):
        assert not session.find("xpath", "//input[@id='form_terms_of_use']").checked

    @pytest.mark.requires("js")
    def test_triggers_associated_events(self, session):
        session.visit("/with_js")
        session.check("checkbox_with_event")
        assert session.has_css("#checkbox_event_triggered")

    def test_checking_does_not_change_an_already_checked_checkbox(self, session):
        assert session.find("xpath", "//input[@id='form_pets_dog']").checked
        session.check("form_pets_dog")
        assert session.find("xpath", "//input[@id='form_pets_dog']").checked

    def test_checking_checks_an_unchecked_checkbox(self, session):
        assert not session.find("xpath", "//input[@id='form_pets_cat']").checked
        session.check("form_pets_cat")
        assert session.find("xpath", "//input[@id='form_pets_cat']").checked

    def test_unchecking_does_not_change_an_already_unchecked_checkbox(self, session):
        assert not session.find("xpath", "//input[@id='form_pets_cat']").checked
        session.uncheck("form_pets_cat")
        assert not session.find("xpath", "//input[@id='form_pets_cat']").checked

    def test_unchecking_unchecks_a_checked_checkbox(self, session):
        assert session.find("xpath", "//input[@id='form_pets_dog']").checked
        session.uncheck("form_pets_dog")
        assert not session.find("xpath", "//input[@id='form_pets_dog']").checked

    def test_checks_a_checkbox_by_id(self, session):
        session.check("form_pets_cat")
        session.click_button("awesome")
        pets = extract_results(session).getlist("form[pets][]")
        assert "dog" in pets
        assert "cat" in pets
        assert "hamster" in pets

    def test_checks_a_checkbox_by_label(self, session):
        session.check("Cat")
        session.click_button("awesome")
        pets = extract_results(session).getlist("form[pets][]")
        assert "dog" in pets
        assert "cat" in pets
        assert "hamster" in pets

    def test_raises_an_error_for_a_locator_that_does_not_exist(self, session):
        with pytest.raises(ElementNotFound):
            session.check("does not exist")

    def test_raises_an_error_for_a_disabled_checkbox(self, session):
        with pytest.raises(ElementNotFound):
            session.check("Disabled Checkbox")


class TestCheckWithAutomaticLabelClick(CheckTestCase):
    @pytest.fixture(autouse=True)
    def setup_settings(self):
        old_automatic_label_click = capybara.automatic_label_click
        capybara.automatic_label_click = True
        try:
            yield
        finally:
            capybara.automatic_label_click = old_automatic_label_click

    def test_checks_via_clicking_the_label_with_for_attribute_if_possible(self, session):
        assert session.find("checkbox", "form_cars_tesla", unchecked=True, visible="hidden")
        session.check("form_cars_tesla")
        session.click_button("awesome")
        assert "tesla" in extract_results(session).getlist("form[cars][]")

    def test_checks_via_clicking_the_wrapping_label_if_possible(self, session):
        assert session.find("checkbox", "form_cars_mclaren", unchecked=True, visible="hidden")
        session.check("form_cars_mclaren")
        session.click_button("awesome")
        assert "mclaren" in extract_results(session).getlist("form[cars][]")

    def test_does_not_click_the_label_if_unneeded(self, session):
        assert session.find("checkbox", "form_cars_jaguar", checked=True, visible="hidden")
        session.check("form_cars_jaguar")
        session.click_button("awesome")
        assert "jaguar" in extract_results(session).getlist("form[cars][]")

    def test_raises_original_error_when_no_label_available(self, session):
        with pytest.raises(ElementNotFound) as excinfo:
            session.check("form_cars_ariel")
        assert "Unable to find checkbox 'form_cars_ariel'" in str(excinfo.value)

    def test_raises_error_if_not_allowed_to_click_label(self, session):
        with pytest.raises(ElementNotFound) as excinfo:
            session.check("form_cars_mclaren", allow_label_click=False)
        assert "Unable to find checkbox 'form_cars_mclaren'" in str(excinfo.value)


class TestCheckWithoutAutomaticLabelClick(CheckTestCase):
    @pytest.fixture(autouse=True)
    def setup_settings(self):
        old_automatic_label_click = capybara.automatic_label_click
        capybara.automatic_label_click = False
        try:
            yield
        finally:
            capybara.automatic_label_click = old_automatic_label_click

    def test_raises_error_if_checkbox_not_visible(self, session):
        with pytest.raises(ElementNotFound) as excinfo:
            session.check("form_cars_mclaren")
        assert "Unable to find checkbox 'form_cars_mclaren'" in str(excinfo.value)

    def test_checks_via_the_label_if_allow_label_click_is_true(self, session):
        assert session.find("checkbox", "form_cars_tesla", unchecked=True, visible="hidden")
        session.check("form_cars_tesla", allow_label_click=True)
        session.click_button("awesome")
        assert "tesla" in extract_results(session).getlist("form[cars][]")
