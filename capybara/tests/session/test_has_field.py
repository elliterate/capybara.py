import pytest
import re


class HasFieldTestCase:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/form")


class TestHasField(HasFieldTestCase):
    def test_is_true_if_the_field_is_on_the_page(self, session):
        assert session.has_field("Dog")
        assert session.has_field("form_description")
        assert session.has_field("Region")

    def test_is_false_if_the_field_is_not_on_the_page(self, session):
        assert not session.has_field("Monkey")

    def test_is_true_if_a_field_with_the_given_value_is_on_the_page(self, session):
        assert session.has_field("First Name", value="John")
        assert session.has_field("First Name", value=re.compile(r"^Joh"))
        assert session.has_field("Phone", value="+1 555 7021")
        assert session.has_field("Street", value="Sesame street 66")
        assert session.has_field("Description", value="Descriptive text goes here")

    def test_is_false_if_a_field_with_the_given_value_is_not_on_the_page(self, session):
        assert not session.has_field("First Name", value="Peter")
        assert not session.has_field("First Name", value=re.compile(r"eter$"))
        assert not session.has_field("Wrong Name", value="John")
        assert not session.has_field("Description", value="Monkey")

    def test_is_true_after_the_field_has_been_filled_in_with_the_given_value(self, session):
        session.fill_in("First Name", value="Jonas")
        assert session.has_field("First Name", value="Jonas")
        assert session.has_field("First Name", value=re.compile(r"ona"))

    def test_is_false_after_the_field_has_been_filled_in_with_a_different_value(self, session):
        session.fill_in("First Name", value="Jonas")
        assert not session.has_field("First Name", value="John")
        assert not session.has_field("First Name", value=re.compile(r"John|Paul|George|Ringo"))


class TestHasFieldDisabled(HasFieldTestCase):
    def test_does_not_find_disabled_fields_when_false(self, session):
        assert not session.has_field("Disabled Checkbox", disabled=False)

    def test_finds_enabled_fields_when_false(self, session):
        assert session.has_field("Dog", disabled=False)

    def test_finds_disabled_fields_when_true(self, session):
        assert session.has_field("Disabled Checkbox", disabled=True)

    def test_does_not_find_enabled_fields_when_true(self, session):
        assert not session.has_field("Dog", disabled=True)

    def test_finds_disabled_fields_when_all(self, session):
        assert session.has_field("Disabled Checkbox", disabled="all")

    def test_finds_enabled_fields_when_all(self, session):
        assert session.has_field("Dog", disabled="all")


class TestHasNoField:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/form")

    def test_is_false_if_the_field_is_on_the_page(self, session):
        assert not session.has_no_field("Dog")
        assert not session.has_no_field("form_description")
        assert not session.has_no_field("Region")

    def test_is_true_if_the_field_is_not_on_the_page(self, session):
        assert session.has_no_field("Monkey")

    def test_is_false_if_a_field_with_the_given_value_is_on_the_page(self, session):
        assert not session.has_no_field("First Name", value="John")
        assert not session.has_no_field("First Name", value=re.compile(r"^Joh"))
        assert not session.has_no_field("Phone", value="+1 555 7021")
        assert not session.has_no_field("Street", value="Sesame street 66")
        assert not session.has_no_field("Description", value="Descriptive text goes here")

    def test_is_true_if_a_field_with_the_given_value_is_not_on_the_page(self, session):
        assert session.has_no_field("First Name", value="Peter")
        assert session.has_no_field("First Name", value=re.compile(r"eter$"))
        assert session.has_no_field("Wrong Name", value="John")
        assert session.has_no_field("Description", value="Monkey")

    def test_is_false_after_the_field_has_been_filled_in_with_the_given_value(self, session):
        session.fill_in("First Name", value="Jonas")
        assert not session.has_no_field("First Name", value="Jonas")
        assert not session.has_no_field("First Name", value=re.compile(r"ona"))

    def test_is_true_after_the_field_has_been_filled_in_with_a_different_value(self, session):
        session.fill_in("First Name", value="Jonas")
        assert session.has_no_field("First Name", value="John")
        assert session.has_no_field("First Name", value=re.compile(r"John|Paul|George|Ringo"))
