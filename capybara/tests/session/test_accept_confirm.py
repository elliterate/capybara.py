import pytest

from capybara.exceptions import ModalNotFound


@pytest.mark.requires("modals")
class TestAcceptConfirm:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_js")

    def test_accepts_the_confirm(self, session):
        with session.accept_confirm():
            session.click_link("Open confirm")
        assert session.has_xpath("//a[@id='open-confirm' and @confirmed='true']")

    def test_raises_an_error_if_no_confirm_found(self, session):
        with pytest.raises(ModalNotFound):
            with session.accept_confirm():
                pass

    def test_accepts_the_confirm_if_the_message_matches(self, session):
        with session.accept_confirm("Confirm opened"):
            session.click_link("Open confirm")
        assert session.has_xpath("//a[@id='open-confirm' and @confirmed='true']")

    def test_raises_an_error_if_the_message_does_not_match(self, session):
        with pytest.raises(ModalNotFound):
            with session.accept_confirm("Incorrect Text"):
                session.click_link("Open confirm")

    def test_works_with_nested_modals(self, session):
        with session.dismiss_confirm("Are you really sure?"):
            with session.accept_confirm("Are you sure?"):
                session.click_link("Open check twice")
        assert session.has_xpath("//a[@id='open-twice' and @confirmed='false']")
