import pytest


class HasSelectTestCase:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/form")


class TestHasSelect(HasSelectTestCase):
    def test_is_true_if_the_field_is_on_the_page(self, session):
        assert session.has_select("Locale")
        assert session.has_select("form_region")
        assert session.has_select("Languages")

    def test_is_false_if_the_field_is_not_on_the_page(self, session):
        assert not session.has_select("Monkey")


class TestHasSelectWithSelected(HasSelectTestCase):
    def test_is_true_if_a_field_with_the_given_value_is_on_the_page(self, session):
        assert session.has_select("form_locale", selected="English")
        assert session.has_select("Region", selected="Norway")
        assert session.has_select("Underwear", selected=[
            "Boxerbriefs", "Briefs", "Commando", "Frenchman's Pantalons", "Long Johns"])

    def test_is_false_if_the_given_field_is_not_on_the_page(self, session):
        assert not session.has_select("Locale", selected="Swedish")
        assert not session.has_select("Does not exist", selected="John")
        assert not session.has_select("City", selected="Not there")
        assert not session.has_select("Underwear", selected=[
            "Boxerbriefs", "Briefs", "Commando", "Frenchman's Pantalons", "Long Johns",
            "Nonexistant"])
        assert not session.has_select("Underwear", selected=[
            "Boxerbriefs", "Briefs", "Boxers", "Commando", "Frenchman's Pantalons", "Long Johns"])
        assert not session.has_select("Underwear", selected=[
            "Boxerbriefs", "Briefs", "Commando", "Frenchman's Pantalons"])

    def test_is_true_after_the_given_value_is_selected(self, session):
        session.select("Swedish", field="Locale")
        assert session.has_select("Locale", selected="Swedish")

    def test_is_false_after_a_different_value_is_selected(self, session):
        session.select("Swedish", field="Locale")
        assert not session.has_select("Locale", selected="English")

    def test_is_true_after_the_given_values_are_selected(self, session):
        session.select("Boxers", field="Underwear")
        assert session.has_select("Underwear", selected=[
            "Boxerbriefs", "Briefs", "Boxers", "Commando", "Frenchman's Pantalons", "Long Johns"])

    def test_is_false_after_one_of_the_values_is_unselected(self, session):
        session.unselect("Briefs", field="Underwear")
        assert not session.has_select("Underwear", selected=[
            "Boxerbriefs", "Briefs", "Commando", "Frenchman's Pantalons", "Long Johns"])

    def test_is_true_even_when_the_selected_option_is_invisible_regardless_of_select_visibility(self, session):
        assert session.has_select("Icecream", visible=False, selected="Chocolate")
        assert session.has_select("Sorbet", selected="Vanilla")


class TestHasSelectWithExactOptions(HasSelectTestCase):
    def test_is_true_if_a_field_with_the_given_options_is_on_the_page(self, session):
        assert session.has_select("Region", options=["Norway", "Sweden", "Finland"])
        assert session.has_select("Tendency", options=[])

    def test_is_false_if_the_given_field_is_not_on_the_page(self, session):
        assert not session.has_select("Locale", options=["Swedish"])
        assert not session.has_select("Does not exist", options=["John"])
        assert not session.has_select("City", options=["London", "Made up city"])
        assert not session.has_select("Region", options=["Norway", "Sweden"])
        assert not session.has_select("Region", options=["Norway", "Norway", "Norway"])

    def test_is_true_even_when_the_options_are_invisible_if_the_select_is_invisible(self, session):
        assert session.has_select("Icecream", visible=False, options=["Chocolate", "Vanilla", "Strawberry"])


class TestHasSelectWithPartialOptions(HasSelectTestCase):
    def test_is_true_if_a_field_with_the_given_partial_options_is_on_the_page(self, session):
        assert session.has_select("Region", with_options=["Norway", "Sweden"])
        assert session.has_select("City", with_options=["London"])

    def test_is_false_if_a_field_with_the_given_partial_options_is_not_on_the_page(self, session):
        assert not session.has_select("Locale", with_options=["Uruguayan"])
        assert not session.has_select("Does not exist", with_options=["John"])
        assert not session.has_select("Region", with_options=["Norway", "Sweden", "Finland", "Latvia"])

    def test_is_true_even_when_the_options_are_invisible_if_the_select_itself_is_invisible(self, session):
        assert session.has_select("Icecream", visible=False, with_options=["Vanilla", "Strawberry"])


class TestHasSelectMultiple(HasSelectTestCase):
    def test_finds_multiple_selects_if_true(self, session):
        assert session.has_select("form_languages", multiple=True)
        assert not session.has_select("form_other_title", multiple=True)

    def test_does_not_find_multiple_selects_if_false(self, session):
        assert not session.has_select("form_languages", multiple=False)
        assert session.has_select("form_other_title", multiple=False)

    def test_finds_both_if_not_specified(self, session):
        assert session.has_select("form_languages")
        assert session.has_select("form_other_title")


class TestHasNoSelect(HasSelectTestCase):
    def test_is_false_if_the_field_is_on_the_page(self, session):
        assert not session.has_no_select("Locale")
        assert not session.has_no_select("form_region")
        assert not session.has_no_select("Languages")

    def test_is_true_if_the_field_is_not_on_the_page(self, session):
        assert session.has_no_select("Monkey")


class TestHasNoSelectWithSelected(HasSelectTestCase):
    def test_is_false_if_a_field_with_the_given_value_is_on_the_page(self, session):
        assert not session.has_no_select("form_locale", selected="English")
        assert not session.has_no_select("Region", selected="Norway")
        assert not session.has_no_select("Underwear", selected=[
            "Boxerbriefs", "Briefs", "Commando", "Frenchman's Pantalons", "Long Johns"])

    def test_is_true_if_the_given_field_is_not_on_the_page(self, session):
        assert session.has_no_select("Locale", selected="Swedish")
        assert session.has_no_select("Does not exist", selected="John")
        assert session.has_no_select("City", selected="Not there")
        assert session.has_no_select("Underwear", selected=[
            "Boxerbriefs", "Briefs", "Commando", "Frenchman's Pantalons", "Long Johns", "Nonexistant"])
        assert session.has_no_select("Underwear", selected=[
            "Boxerbriefs", "Briefs", "Boxers", "Commando", "Frenchman's Pantalons", "Long Johns"])
        assert session.has_no_select("Underwear", selected=[
            "Boxerbriefs", "Briefs", "Commando", "Frenchman's Pantalons"])

    def test_is_false_after_the_given_value_is_selected(self, session):
        session.select("Swedish", field="Locale")
        assert not session.has_no_select("Locale", selected="Swedish")

    def test_is_true_after_a_different_value_is_selected(self, session):
        session.select("Swedish", field="Locale")
        assert session.has_no_select("Locale", selected="English")

    def test_is_false_after_the_given_values_are_selected(self, session):
        session.select("Boxers", field="Underwear")
        assert not session.has_no_select("Underwear", selected=[
            "Boxerbriefs", "Briefs", "Boxers", "Commando", "Frenchman's Pantalons", "Long Johns"])

    def test_is_true_after_one_of_the_values_is_unselected(self, session):
        session.unselect("Briefs", field="Underwear")
        assert session.has_no_select("Underwear", selected=[
            "Boxerbriefs", "Briefs", "Commando", "Frenchman's Pantalons", "Long Johns"])


class TestHasNoSelectWithExactOptions(HasSelectTestCase):
    def test_is_false_if_a_field_with_the_given_options_is_on_the_page(self, session):
        assert not session.has_no_select("Region", options=["Norway", "Sweden", "Finland"])

    def test_is_true_if_the_given_field_is_not_on_the_page(self, session):
        assert session.has_no_select("Locale", options=["Swedish"])
        assert session.has_no_select("Does not exist", options=["John"])
        assert session.has_no_select("City", options=["London", "Made up city"])
        assert session.has_no_select("Region", options=["Norway", "Sweden"])
        assert session.has_no_select("Region", options=["Norway", "Norway", "Norway"])


class TestHasNoSelectWithPartialOptions(HasSelectTestCase):
    def test_is_false_if_a_field_with_the_given_partial_options_is_on_the_page(self, session):
        assert not session.has_no_select("Region", with_options=["Norway", "Sweden"])
        assert not session.has_no_select("City", with_options=["London"])

    def test_is_true_if_a_field_with_the_given_partial_options_is_not_on_the_page(self, session):
        assert session.has_no_select("Locale", with_options=["Uruguayan"])
        assert session.has_no_select("Does not exist", with_options=["John"])
        assert session.has_no_select("Region", with_options=["Norway", "Sweden", "Finland", "Latvia"])
