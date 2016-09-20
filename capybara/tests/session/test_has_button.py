import pytest


class HasButtonTestCase:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/form")


class TestHasButton(HasButtonTestCase):
    def test_is_true_if_the_given_button_is_on_the_page(self, session):
        assert session.has_button("med")
        assert session.has_button("crap321")

    def test_is_false_if_the_given_button_is_not_on_the_page(self, session):
        assert not session.has_button("monkey")

    def test_is_false_if_the_given_button_is_disabled(self, session):
        assert not session.has_button("Disabled button")


class TestHasButtonDisabled(HasButtonTestCase):
    def test_is_false_for_disabled_buttons_when_false(self, session):
        assert not session.has_button("Disabled button", disabled=False)

    def test_is_true_for_enabled_buttons_when_false(self, session):
        assert session.has_button("med", disabled=False)

    def test_is_true_for_disabled_buttons_when_true(self, session):
        assert session.has_button("Disabled button", disabled=True)

    def test_is_false_for_enabled_buttons_when_true(self, session):
        assert not session.has_button("med", disabled=True)

    def test_is_true_for_disabled_buttons_when_all(self, session):
        assert session.has_button("Disabled button", disabled="all")

    def test_is_true_for_enabled_buttons_when_all(self, session):
        assert session.has_button("med", disabled="all")


class TestHasNoButton:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/form")

    def test_is_false_if_the_given_button_is_on_the_page(self, session):
        assert not session.has_no_button("med")
        assert not session.has_no_button("crap321")

    def test_is_false_for_disabled_buttons_if_disabled_is_true(self, session):
        assert not session.has_no_button("Disabled button", disabled=True)

    def test_is_true_if_the_given_button_is_not_on_the_page(self, session):
        assert session.has_no_button("monkey")

    def test_is_true_for_disabled_buttons_by_default(self, session):
        assert session.has_no_button("Disabled button")

    def test_is_true_for_disabled_buttons_if_disabled_is_false(self, session):
        assert session.has_no_button("Disabled button", disabled=False)
