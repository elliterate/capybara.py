import pytest
import re

from capybara.exceptions import ElementNotFound
from capybara.tests.helpers import extract_results


class ClickButtonTestCase:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/form")


class TestClickButton(ClickButtonTestCase):
    @pytest.mark.requires("js")
    def test_waits_for_asynchronous_load(self, session):
        session.visit("/with_js")
        session.click_link("Click me")
        session.click_button("New Here")

    def test_submits_the_latest_given_value_with_multiple_values_of_the_same_name(self, session):
        session.check("Terms of Use")
        session.click_button("awesome")
        assert extract_results(session).getlist("form[terms_of_use]")[-1] == "1"

    def test_submits_form_for_submit_button_by_id(self, session):
        session.click_button("awe123")
        assert extract_results(session)["form[first_name]"] == "John"

    def test_submits_form_for_submit_button_by_title(self, session):
        session.click_button("What an Awesome Button")
        assert extract_results(session)["form[first_name]"] == "John"

    def test_submits_form_for_submit_button_by_partial_title(self, session):
        session.click_button("What an Awesome")
        assert extract_results(session)["form[first_name]"] == "John"

    def test_raises_an_error_for_partial_title_when_exact_is_true(self, session):
        with pytest.raises(ElementNotFound):
            session.click_button("What an Awesome", exact=True)

    def test_submits_form1_for_associated_button_located_within_form2(self, session):
        session.click_button("other_form_button")
        assert extract_results(session)["form[which_form]"] == "form1"

    def test_does_not_error_when_submit_button_not_associated_with_any_form_is_clicked(self, session):
        session.click_button("no_form_button")

    def test_submits_form_for_image_button_with_alt(self, session):
        session.click_button("oh hai thar")
        assert extract_results(session)["form[first_name]"] == "John"

    def test_submits_form_for_image_button_with_partial_alt(self, session):
        session.click_button("hai")
        assert extract_results(session)["form[first_name]"] == "John"

    def test_submits_form_for_image_button_with_value(self, session):
        session.click_button("okay")
        assert extract_results(session)["form[first_name]"] == "John"

    def test_submits_form_for_image_button_with_partial_value(self, session):
        session.click_button("kay")
        assert extract_results(session)["form[first_name]"] == "John"

    def test_submits_form_for_image_button_with_id(self, session):
        session.click_button("okay556")
        assert extract_results(session)["form[first_name]"] == "John"

    def test_submits_form_for_image_button_with_title(self, session):
        session.click_button("Okay 556 Image")
        assert extract_results(session)["form[first_name]"] == "John"

    def test_submits_form_for_image_button_with_partial_title(self, session):
        session.click_button("Okay 556")
        assert extract_results(session)["form[first_name]"] == "John"

    def test_submits_form_for_button_tag_with_text(self, session):
        session.click_button("Click me")
        assert extract_results(session)["form[first_name]"] == "John"

    def test_submits_form_for_button_tag_with_partial_text(self, session):
        session.click_button("Click")
        assert extract_results(session)["form[first_name]"] == "John"

    def test_submits_form_for_button_tag_with_id(self, session):
        session.click_button("click_me_123")
        assert extract_results(session)["form[first_name]"] == "John"

    def test_submits_form_for_button_tag_with_value(self, session):
        session.click_button("click_me")
        assert extract_results(session)["form[first_name]"] == "John"

    def test_submits_form_for_button_tag_with_partial_value(self, session):
        session.click_button("ck_me")
        assert extract_results(session)["form[first_name]"] == "John"

    def test_submits_form_for_button_tag_with_title(self, session):
        session.click_button("Click Title button")
        assert extract_results(session)["form[first_name]"] == "John"

    def test_submits_form_for_button_tag_with_partial_title(self, session):
        session.click_button("Click Title")
        assert extract_results(session)["form[first_name]"] == "John"

    def test_submits_form_for_button_tag_with_descendant_image_alt(self, session):
        session.click_button("A horse eating hay")
        assert extract_results(session)["form[first_name]"] == "John"

    def test_submits_form_for_button_tag_with_partial_descendant_image_alt(self, session):
        session.click_button("se eating h")
        assert extract_results(session)["form[first_name]"] == "John"

    def test_raises_an_error_for_locator_that_does_not_exist(self, session):
        with pytest.raises(ElementNotFound) as excinfo:
            session.click_button("does not exist")
        assert "Unable to find button 'does not exist'" in str(excinfo.value)

    def test_serializes_and_sends_valueless_buttons_that_were_clicked(self, session):
        session.click_button("No Value!")
        assert extract_results(session)["form[no_value]"] is not None

    def test_does_not_send_image_buttons_that_were_not_clicked(self, session):
        session.click_button("awesome")
        assert extract_results(session).get("form[okay]") is None

    def test_serializes_and_sends_get_forms(self, session):
        session.visit("/form")
        session.click_button("med")
        results = extract_results(session)
        assert results["form[middle_name]"] == "Darren"
        assert results.get("form[foo]") is None

    def test_follows_redirects(self, session):
        session.click_button("Go FAR")
        assert session.has_text("You landed")
        assert re.compile(r"/landed$").search(session.current_url)

    def test_posts_back_to_the_same_url_when_no_action_given(self, session):
        session.visit("/postback")
        session.click_button("With no action")
        assert session.has_text("Postback")

    def test_raises_an_error_for_disabled_buttons(self, session):
        with pytest.raises(ElementNotFound):
            session.click_button("Disabled button")

    def test_encodes_complex_field_names(self, session):
        session.fill_in("address1_city", value="Paris")
        session.fill_in("address1_street", value="CDG")

        session.fill_in("address2_city", value="Mikolaiv")
        session.fill_in("address2_street", value="PGS")

        session.click_button("awesome")

        results = extract_results(session)

        assert results.getlist("form[addresses][][street]") == ["CDG", "PGS"]
        assert results.getlist("form[addresses][][city]") == ["Paris", "Mikolaiv"]
        assert results.getlist("form[addresses][][country]") == ["France", "Ukraine"]


class TestClickSubmitButtonWithHTML5Fields(ClickButtonTestCase):
    @pytest.fixture
    def results(self, session):
        session.click_button("html5_submit")
        return extract_results(session)

    def test_serializes_and_submits_search_fields(self, results):
        assert results["form[html5_search]"] == "what are you looking for"

    def test_serializes_and_submits_email_fields(self, results):
        assert results["form[html5_email]"] == "person@email.com"

    def test_serializes_and_submits_url_fields(self, results):
        assert results["form[html5_url]"] == "http://www.example.com"

    def test_serializes_and_submits_tel_fields(self, results):
        assert results["form[html5_tel]"] == "911"

    def test_serializes_and_submits_color_fields(self, results):
        assert results["form[html5_color]"].upper() == "#FFFFFF"


class TestClickSubmitButtonWithHTML4Fields(ClickButtonTestCase):
    @pytest.fixture
    def results(self, session):
        session.click_button("awesome")
        return extract_results(session)

    def test_serializes_and_submits_text_fields(self, results):
        assert results["form[first_name]"] == "John"

    def test_escapes_fields_when_submitting(self, results):
        assert results["form[phone]"] == "+1 555 7021"

    def test_serializes_and_submits_password_fields(self, results):
        assert results["form[password]"] == "seeekrit"

    def test_serializes_and_submits_hidden_fields(self, results):
        assert results["form[token]"] == "12345"

    def test_does_not_serialize_fields_from_other_forms(self, results):
        assert results.get("form[middle_name]") is None

    def test_submits_the_button_that_was_clicked_but_not_other_buttons(self, results):
        assert results["form[awesome]"] == "awesome"
        assert results.get("form[crappy]") is None

    def test_serializes_radio_buttons(self, results):
        assert results["form[gender]"] == "female"

    def test_defaults_radio_values_to_on_if_none_specified(self, results):
        assert results["form[valueless_radio]"] == "on"

    def test_serializes_check_boxes(self, results):
        assert "dog" in results.getlist("form[pets][]")
        assert "hamster" in results.getlist("form[pets][]")
        assert "cat" not in results.getlist("form[pets][]")

    def test_defaults_checkbox_value_to_on_if_none_specified(self, results):
        assert results["form[valueless_checkbox]"] == "on"

    def test_serializes_text_areas(self, results):
        assert results["form[description]"] == "Descriptive text goes here"

    def test_serializes_select_tag_with_values(self, results):
        assert results["form[locale]"] == "en"

    def test_serializes_select_tag_without_values(self, results):
        assert results["form[region]"] == "Norway"

    def test_serializes_first_option_for_select_tag_with_no_selection(self, results):
        assert results["form[city]"] == "London"

    def test_does_not_serialize_a_select_tag_without_options(self, results):
        assert results.get("form[tendency]") is None

    def test_converts_lf_to_cr_lf_in_submitted_textareas(self, results):
        assert results["form[newline]"] == "\r\nNew line after and before textarea tag\r\n"

    def test_does_not_submit_disabled_fields(self, results):
        assert results.get("form[disabled_text_field]") is None
        assert results.get("form[disabled_textarea]") is None
        assert results.get("form[disabled_checkbox]") is None
        assert results.get("form[disabled_radio]") is None
        assert results.get("form[disabled_select]") is None
        assert results.get("form[disabled_file]") is None


class TestClickButtonWithAssociatedFormFields(ClickButtonTestCase):
    @pytest.fixture
    def results(self, session):
        session.click_button("submit_form1")
        return extract_results(session)

    def test_serializes_and_submits_text_fields(self, results):
        assert results["form[outside_input]"] == "outside_input"

    def test_serializes_text_areas(self, results):
        assert results["form[outside_textarea]"] == "Some text here"

    def test_serializes_select_tags(self, results):
        assert results["form[outside_select]"] == "Ruby"

    def test_does_not_serialize_fields_associated_with_a_different_form(self, results):
        assert results.get("form[for_form2]") is None


class TestClickButtonTagOutsideForm(ClickButtonTestCase):
    @pytest.fixture
    def results(self, session):
        session.click_button("outside_button")
        return extract_results(session)

    def test_submits_the_associated_form(self, results):
        assert results["form[which_form]"] == "form2"

    def test_submits_the_button_that_was_clicked_but_not_other_buttons(self, results):
        assert results["form[outside_button]"] == "outside_button"
        assert results.get("form[unused]") is None


class TestClickSubmitTypeInputTagOutsideForm(ClickButtonTestCase):
    @pytest.fixture
    def results(self, session):
        session.click_button("outside_submit")
        return extract_results(session)

    def test_submits_the_associated_form(self, results):
        assert results["form[which_form]"] == "form1"

    def test_submits_the_button_that_was_clicked_but_not_other_buttons(self, results):
        assert results["form[outside_submit]"] == "outside_submit"
        assert results.get("form[submit_form1]") is None
