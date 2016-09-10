import pytest

from capybara.exceptions import ElementNotFound


class SelectorTestCase:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/form")


class TestLabelSelector(SelectorTestCase):
    def test_finds_a_label_by_text(self, session):
        assert session.find("label", "Customer Name").text == "Customer Name"

    def test_finds_a_label_by_for_attribute_string(self, session):
        assert session.find("label", field="form_other_title")["for"] == "form_other_title"

    def test_finds_a_label_from_nested_input_using_field_filter(self, session):
        field = session.find("id", "nested_label")
        assert session.find("label", field=field).text == "Nested Label"

    def test_finds_the_label_for_a_non_nested_element_using_field_filter(self, session):
        field = session.find("id", "form_other_title")
        assert session.find("label", field=field)["for"] == "form_other_title"

    def test_matches_substrings_when_exact_is_false(self, session):
        assert session.find("label", "Customer Na", exact=False).text == "Customer Name"

    def test_does_not_match_substrings_when_exact_is_true(self, session):
        with pytest.raises(ElementNotFound):
            session.find("label", "Customer Na", exact=True)
