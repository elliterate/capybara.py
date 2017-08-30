import pytest

import capybara
from capybara.exceptions import ElementNotFound


class FindButtonTestCase:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/form")


class TestFindButton(FindButtonTestCase):
    def test_finds_any_button(self, session):
        assert session.find_button("med")["id"] == "mediocre"
        assert session.find_button("crap321").value == "crappy"

    def test_raises_an_error_if_the_button_does_not_exist(self, session):
        with pytest.raises(ElementNotFound):
            session.find_button("Does not exist")

    def test_raises_an_error_if_the_button_is_disabled(self, session):
        with pytest.raises(ElementNotFound):
            session.find_button("Disabled button")

    def test_finds_by_aria_label_attribute_when_enable_aria_label_is_true(self, session):
        capybara.enable_aria_label = True
        assert session.find_button("Mediocre Button")["id"] == "mediocre"

    def test_does_not_find_by_aria_label_attribute_when_enable_aria_label_is_false(self, session):
        capybara.enable_aria_label = False
        with pytest.raises(ElementNotFound):
            session.find_button("Mediocre Button")

    def test_uses_options_without_locator(self, session):
        assert session.find_button(disabled=True).value == "Disabled button"


class TestFindButtonDisabled(FindButtonTestCase):
    def test_does_not_find_disabled_buttons_when_false(self, session):
        with pytest.raises(ElementNotFound):
            session.find_button("Disabled button", disabled=False)

    def test_finds_enabled_buttons_when_false(self, session):
        assert session.find_button("med", disabled=False)["id"] == "mediocre"

    def test_finds_disabled_buttons_when_true(self, session):
        field = session.find_button("Disabled button", disabled=True)
        assert field.value == "Disabled button"

    def test_does_not_find_enabled_buttons_when_true(self, session):
        with pytest.raises(ElementNotFound):
            session.find_button("med", disabled=True)

    def test_finds_disabled_buttons_when_all(self, session):
        field = session.find_button("Disabled button", disabled="all")
        assert field.value == "Disabled button"

    def test_finds_enabled_buttons_when_all(self, session):
        assert session.find_button("med", disabled="all")["id"] == "mediocre"
