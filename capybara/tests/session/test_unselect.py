import pytest

from capybara.exceptions import ElementNotFound, UnselectNotAllowed
from capybara.tests.helpers import extract_results


class TestUnselect:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/form")

    def test_raises_an_error_with_single_select(self, session):
        with pytest.raises(UnselectNotAllowed):
            session.unselect("English", field="form_locale")

    def test_raises_an_error_with_a_locator_that_does_not_exist(self, session):
        with pytest.raises(ElementNotFound):
            session.unselect("foo", field="does not exist")

    def test_raises_an_error_with_an_option_that_does_not_exist(self, session):
        with pytest.raises(ElementNotFound):
            session.unselect("Does not Exist", field="form_underwear")

    def test_approximately_matches_select_box(self, session):
        session.unselect("Boxerbriefs", field="Under")
        session.click_button("awesome")
        underwear = extract_results(session).getlist("form[underwear][]")
        assert "Boxerbriefs" not in underwear

    def test_approximately_matches_option(self, session):
        session.unselect("Boxerbr", field="Underwear")
        session.click_button("awesome")
        underwear = extract_results(session).getlist("form[underwear][]")
        assert "Boxerbriefs" not in underwear

    def test_approximately_matches_when_field_not_given(self, session):
        session.unselect("Boxerbr")
        session.click_button("awesome")
        underwear = extract_results(session).getlist("form[underwear][]")
        assert "Boxerbriefs" not in underwear

    def test_does_not_approximately_match_select_box(self, session):
        with pytest.raises(ElementNotFound):
            session.unselect("Boxerbriefs", field="Under", exact=True)

    def test_does_not_approximately_match_option(self, session):
        with pytest.raises(ElementNotFound):
            session.unselect("Boxerbr", field="Underwear", exact=True)

    def test_does_not_approximately_match_when_field_not_given(self, session):
        with pytest.raises(ElementNotFound):
            session.unselect("Boxerbr", exact=True)


class TestMultipleUnselect:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/form")

    def test_unselects_an_option_from_a_select_box_by_id(self, session):
        session.unselect("Commando", field="form_underwear")
        session.click_button("awesome")
        underwear = extract_results(session).getlist("form[underwear][]")
        assert "Briefs" in underwear
        assert "Boxerbriefs" in underwear
        assert "Command" not in underwear

    def test_unselects_an_option_without_a_select_box(self, session):
        session.unselect("Commando")
        session.click_button("awesome")
        underwear = extract_results(session).getlist("form[underwear][]")
        assert "Briefs" in underwear
        assert "Boxerbriefs" in underwear
        assert "Command" not in underwear

    def test_unselects_an_option_from_a_select_box_by_label(self, session):
        session.unselect("Commando", field="Underwear")
        session.click_button("awesome")
        underwear = extract_results(session).getlist("form[underwear][]")
        assert "Briefs" in underwear
        assert "Boxerbriefs" in underwear
        assert "Command" not in underwear

    def test_escapes_quotes(self, session):
        session.unselect("Frenchman's Pantalons", field="Underwear")
        session.click_button("awesome")
        underwear = extract_results(session).getlist("form[underwear][]")
        assert "Frenchman's Pantalons" not in underwear
