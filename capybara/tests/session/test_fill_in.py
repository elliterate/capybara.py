import pytest

from capybara.exceptions import ElementNotFound
from capybara.tests.helpers import extract_results


class TestFillIn:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/form")

    def test_fills_in_a_text_field_by_id(self, session):
        session.fill_in("form_first_name", value="Harry")
        session.click_button("awesome")
        assert extract_results(session)["form[first_name]"] == "Harry"

    def test_fills_in_a_text_field_by_name(self, session):
        session.fill_in("form[last_name]", value="Green")
        session.click_button("awesome")
        assert extract_results(session)["form[last_name]"] == "Green"

    def test_fills_in_a_text_field_by_label_without_for(self, session):
        session.fill_in("First Name", value="Harry")
        session.click_button("awesome")
        assert extract_results(session)["form[first_name]"] == "Harry"

    def test_fills_in_a_url_field_by_label_without_for(self, session):
        session.fill_in("Html5 Url", value="http://www.avenueq.com")
        session.click_button("html5_submit")
        assert extract_results(session)["form[html5_url]"] == "http://www.avenueq.com"

    def test_fills_in_a_textarea_by_id(self, session):
        session.fill_in("form_description", value="Texty text")
        session.click_button("awesome")
        assert extract_results(session)["form[description]"] == "Texty text"

    def test_fills_in_a_textarea_by_label(self, session):
        session.fill_in("Description", value="Texty text")
        session.click_button("awesome")
        assert extract_results(session)["form[description]"] == "Texty text"

    def test_fills_in_a_textarea_by_name(self, session):
        session.fill_in("form[description]", value="Texty text")
        session.click_button("awesome")
        assert extract_results(session)["form[description]"] == "Texty text"

    def test_fills_in_a_password_field_by_id(self, session):
        session.fill_in("form_password", value="supasikrit")
        session.click_button("awesome")
        assert extract_results(session)["form[password]"] == "supasikrit"

    def test_fills_in_a_password_field_by_label(self, session):
        session.fill_in("Password", value="supasikrit")
        session.click_button("awesome")
        assert extract_results(session)["form[password]"] == "supasikrit"

    def test_fills_in_a_password_field_by_name(self, session):
        session.fill_in("form[password]", value="supasikrit")
        session.click_button("awesome")
        assert extract_results(session)["form[password]"] == "supasikrit"

    def test_fills_in_a_field_based_on_current_value(self, session):
        session.fill_in(current_value="John", value="Thomas")
        session.click_button("awesome")
        assert extract_results(session)["form[first_name]"] == "Thomas"

    def test_handles_html_in_a_textarea(self, session):
        session.fill_in("form_description", value="is <strong>very</strong> secret!")
        session.click_button("awesome")
        assert extract_results(session)["form[description]"] == "is <strong>very</strong> secret!"

    def test_handles_newlines_in_a_textarea(self, session):
        session.fill_in("form_description", value="\nSome text\n")
        session.click_button("awesome")
        assert extract_results(session)["form[description]"] == "\r\nSome text\r\n"

    def test_fills_in_a_field_with_a_custom_type(self, session):
        session.fill_in("Schmooo", value="Schmooo is the game")
        session.click_button("awesome")
        assert extract_results(session)["form[schmooo]"] == "Schmooo is the game"

    def test_fills_in_a_field_without_a_type(self, session):
        session.fill_in("Phone", value="+1 555 7022")
        session.click_button("awesome")
        assert extract_results(session)["form[phone]"] == "+1 555 7022"

    def test_fills_in_a_text_field_respecting_its_maxlength_attribute(self, session):
        session.fill_in("Zipcode", value="52071350")
        session.click_button("awesome")
        assert extract_results(session)["form[zipcode]"] == "52071"

    @pytest.mark.requires("js")
    def test_waits_for_asynchronous_load(self, session):
        session.visit("/with_js")
        session.click_link("Click me")
        session.fill_in("new_field", value="Testing...")

    def test_raises_an_error_with_a_locator_that_does_not_exist(self, session):
        with pytest.raises(ElementNotFound):
            session.fill_in("does not exist", value="Blah blah")

    def test_raises_an_error_for_a_disabled_field(self, session):
        with pytest.raises(ElementNotFound):
            session.fill_in("Disabled Text Field", value="Blah blah")

    def test_fills_in_an_approximately_matched_field(self, session):
        session.fill_in("Explanation", value="Dude")
        session.click_button("awesome")
        assert extract_results(session)["form[name_explanation]"] == "Dude"

    def test_raises_an_error_for_an_approximately_matched_field_when_exact_is_true(self, session):
        with pytest.raises(ElementNotFound):
            session.fill_in("Explanation", value="Dude", exact=True)
