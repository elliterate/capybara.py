import pytest

from capybara.exceptions import ModalNotFound


@pytest.mark.requires("modals")
class TestDismissConfirm:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_js")

    def test_dismisses_the_confirm(self, session):
        with session.dismiss_confirm():
            session.click_link("Open confirm")
        assert session.has_xpath("//a[@id='open-confirm' and @confirmed='false']")

    def test_raises_an_error_if_no_confirm_found(self, session):
        with pytest.raises(ModalNotFound):
            with session.dismiss_confirm():
                pass

    def test_dismisses_the_confirm_if_the_message_matches(self, session):
        with session.dismiss_confirm("Confirm opened"):
            session.click_link("Open confirm")
        assert session.has_xpath("//a[@id='open-confirm' and @confirmed='false']")

    def test_raises_an_error_if_the_message_does_not_match(self, session):
        with pytest.raises(ModalNotFound):
            with session.dismiss_confirm("Incorrect Text"):
                session.click_link("Open confirm")
