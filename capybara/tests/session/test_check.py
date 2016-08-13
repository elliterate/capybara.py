import pytest

from capybara.exceptions import ElementNotFound
from capybara.tests.helpers import extract_results


class TestCheck:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/form")

    def test_checked_attribute_s_true_if_checked(self, session):
        session.check("Terms of Use")
        assert session.find("xpath", "//input[@id='form_terms_of_use']").checked

    def test_checked_attribute_is_false_if_unchecked(self, session):
        assert not session.find("xpath", "//input[@id='form_terms_of_use']").checked

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
