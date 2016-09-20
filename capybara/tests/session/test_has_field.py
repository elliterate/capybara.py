import pytest


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
