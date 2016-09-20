import pytest


class TestHasUncheckedField:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/form")

    def test_is_false_if_a_checked_field_is_on_the_page(self, session):
        assert not session.has_unchecked_field("gender_female")
        assert not session.has_unchecked_field("Hamster")

    def test_is_true_if_an_unchecked_field_is_on_the_page(self, session):
        assert session.has_unchecked_field("form_pets_cat")
        assert session.has_unchecked_field("Male")

    def test_is_true_for_disabled_unchecked_fields_if_disabled_is_true(self, session):
        assert session.has_unchecked_field("Disabled Unchecked Checkbox", disabled=True)

    def test_is_false_if_no_field_is_on_the_page(self, session):
        assert not session.has_unchecked_field("Does Not Exist")

    def test_is_false_for_disabled_unchecked_fields_by_default(self, session):
        assert not session.has_unchecked_field("Disabled Unchecked Checkbox")

    def test_is_false_for_disabled_unchecked_fields_if_disabled_is_false(self, session):
        assert not session.has_unchecked_field("Disabled Unchecked Checkbox", disabled=False)

    def test_is_false_after_an_unchecked_checkbox_is_checked(self, session):
        session.check("form_pets_cat")
        assert not session.has_unchecked_field("form_pets_cat")

    def test_is_true_after_a_checked_checkbox_is_unchecked(self, session):
        session.uncheck("form_pets_dog")
        assert session.has_unchecked_field("form_pets_dog")

    def test_is_false_after_an_unchecked_radio_button_is_chosen(self, session):
        session.choose("gender_male")
        assert not session.has_unchecked_field("gender_male")

    def test_is_true_after_another_radio_button_in_the_group_is_chosen(self, session):
        session.choose("gender_male")
        assert session.has_unchecked_field("gender_female")


class TestHasNoUncheckedField:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/form")

    def test_is_true_if_a_checked_field_is_on_the_page(self, session):
        assert session.has_no_unchecked_field("gender_female")
        assert session.has_no_unchecked_field("Hamster")

    def test_is_false_if_an_unchecked_field_is_on_the_page(self, session):
        assert not session.has_no_unchecked_field("form_pets_cat")
        assert not session.has_no_unchecked_field("Male")

    def test_is_false_for_disabled_unchecked_fields_if_disabled_is_true(self, session):
        assert not session.has_no_unchecked_field("Disabled Unchecked Checkbox", disabled=True)

    def test_is_true_if_no_field_is_on_the_page(self, session):
        assert session.has_no_unchecked_field("Does Not Exist")

    def test_is_true_for_disabled_unchecked_fields_by_default(self, session):
        assert session.has_no_unchecked_field("Disabled Unchecked Checkbox")

    def test_is_true_for_disabled_unchecked_fields_if_disabled_is_false(self, session):
        assert session.has_no_unchecked_field("Disabled Unchecked Checkbox", disabled=False)

    def test_is_true_after_an_unchecked_checkbox_is_checked(self, session):
        session.check("form_pets_cat")
        assert session.has_no_unchecked_field("form_pets_cat")

    def test_is_false_after_a_checked_checkbox_is_unchecked(self, session):
        session.uncheck("form_pets_dog")
        assert not session.has_no_unchecked_field("form_pets_dog")

    def test_is_true_after_an_unchecked_radio_button_is_chosen(self, session):
        session.choose("gender_male")
        assert session.has_no_unchecked_field("gender_male")

    def test_is_false_after_another_radio_button_in_the_group_is_chosen(self, session):
        session.choose("gender_male")
        assert not session.has_no_unchecked_field("gender_female")
