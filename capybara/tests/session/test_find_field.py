import pytest

from capybara.exceptions import ElementNotFound


class TestFindField:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/form")

    def test_finds_any_field(self, session):
        assert session.find_field("Dog").value == "dog"
        assert session.find_field("form_description").text == "Descriptive text goes here"
        assert session.find_field("Region")["name"] == "form[region]"

    def test_raises_an_error_if_the_field_does_not_exist(self, session):
        with pytest.raises(ElementNotFound):
            session.find_field("Does not exist")

    def test_finds_an_approximately_matching_field(self, session):
        assert session.find_field("Explanation")["name"] == "form[name_explanation]"

    def test_does_not_find_an_approximately_matching_field_when_exact_is_true(self, session):
        with pytest.raises(ElementNotFound):
            session.find_field("Explanation", exact=True)
