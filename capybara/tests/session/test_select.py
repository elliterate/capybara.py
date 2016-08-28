import pytest

from capybara.exceptions import ElementNotFound
from capybara.tests.helpers import extract_results


class TestSelect:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/form")

    def test_returns_the_value_of_the_first_option(self, session):
        assert session.find_field("Title").value == "Mrs"

    def test_returns_the_value_of_the_selected_option(self, session):
        session.select("Miss", field="Title")
        assert session.find_field("Title").value == "Miss"

    def test_allows_selecting_options_where_they_are_the_only_inexact_match(self, session):
        session.select("Mis", field="Title")
        assert session.find_field("Title").value == "Miss"

    def test_returns_the_value_attribute_rather_than_content_if_present(self, session):
        assert session.find_field("Locale").value == "en"

    def test_selects_an_option_from_a_select_box_by_id(self, session):
        session.select("Finish", field="form_locale")
        session.click_button("awesome")
        assert extract_results(session)["form[locale]"] == "fi"

    def test_selects_an_option_from_a_select_box_by_label(self, session):
        session.select("Finish", field="Locale")
        session.click_button("awesome")
        assert extract_results(session)["form[locale]"] == "fi"

    def test_selects_an_option_without_giving_a_select_box(self, session):
        session.select("Swedish")
        session.click_button("awesome")
        assert extract_results(session)["form[locale]"] == "sv"

    def test_escapes_quotes(self, session):
        session.select("John's made-up language", field="Locale")
        session.click_button("awesome")
        assert extract_results(session)["form[locale]"] == "jo"

    def test_obeys_field(self, session):
        session.select("Miss", field="Other title")
        session.click_button("awesome")
        results = extract_results(session)
        assert results["form[other_title]"] == "Miss"
        assert results["form[title]"] != "Miss"

    def test_matches_labels_with_preceding_or_trailing_whitespace(self, session):
        session.select("Lojban", field="Locale")
        session.click_button("awesome")
        assert extract_results(session)["form[locale]"] == "jbo"

    def test_raises_an_error_with_a_locator_that_does_not_exist(self, session):
        with pytest.raises(ElementNotFound):
            session.select("foo", field="does not exist")

    def test_raises_an_error_with_an_option_that_does_not_exist(self, session):
        with pytest.raises(ElementNotFound):
            session.select("Does not Exist", field="form_locale")

    def test_raises_an_error_for_a_disabled_select(self, session):
        with pytest.raises(ElementNotFound):
            session.select("Should not see me", field="Disabled Select")

    def test_does_not_select_a_disabled_option(self, session):
        with pytest.warns(None) as record:
            session.select("Other", field="form_title")
        assert len(record) == 1
        assert "Attempt to select disabled option" in record[0].message.args[0]
        assert session.find_field("form_title").value != "Other"

    def test_approximately_matches_select_box(self, session):
        session.select("Finish", field="Loc")
        session.click_button("awesome")
        assert extract_results(session)["form[locale]"] == "fi"

    def test_approximately_matches_option(self, session):
        session.select("Fin", field="Locale")
        session.click_button("awesome")
        assert extract_results(session)["form[locale]"] == "fi"

    def test_approximately_matches_option_when_field_not_given(self, session):
        session.select("made-up language")
        session.click_button("awesome")
        assert extract_results(session)["form[locale]"] == "jo"

    def test_does_not_approximately_match_select_box_if_exact_is_true(self, session):
        with pytest.raises(ElementNotFound):
            session.select("Finish", field="Loc", exact=True)

    def test_does_not_approximately_match_option_if_exact_is_true(self, session):
        with pytest.raises(ElementNotFound):
            session.select("Fin", field="Locale", exact=True)

    def test_does_not_approximately_match_option_when_field_not_given_if_exact_is_true(self, session):
        with pytest.raises(ElementNotFound):
            session.select("made-up language", exact=True)


class TestMultipleSelect:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/form")

    def test_returns_an_empty_value(self, session):
        assert session.find_field("Language").value == []

    def test_returns_the_value_of_the_selected_options(self, session):
        session.select("Ruby", field="Language")
        session.select("Javascript", field="Language")
        languages = session.find_field("Language").value
        assert "Ruby" in languages
        assert "Javascript" in languages

    def test_selects_one_option(self, session):
        session.select("Ruby", field="Language")
        session.click_button("awesome")
        assert extract_results(session).getlist("form[languages][]") == ["Ruby"]

    def test_selects_multiple_options(self, session):
        session.select("Ruby", field="Language")
        session.select("Javascript", field="Language")
        session.click_button("awesome")
        languages = extract_results(session).getlist("form[languages][]")
        assert "Ruby" in languages
        assert "Javascript" in languages

    def test_remains_selected_if_already_selected(self, session):
        session.select("Ruby", field="Language")
        session.select("Javascript", field="Language")
        session.select("Ruby", field="Language")
        session.click_button("awesome")
        languages = extract_results(session).getlist("form[languages][]")
        assert "Ruby" in languages
        assert "Javascript" in languages

    def test_returns_value_attribute_rather_than_content_if_present(self, session):
        assert "thermal" in session.find_field("Underwear").value
