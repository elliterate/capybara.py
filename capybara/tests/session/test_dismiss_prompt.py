import pytest

from capybara.exceptions import ModalNotFound


@pytest.mark.requires("modals")
class TestDismissPrompt:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_js")

    def test_dismisses_the_prompt(self, session):
        with session.dismiss_prompt():
            session.click_link("Open prompt")
        assert session.has_xpath("//a[@id='open-prompt' and @response='dismissed']")

    def test_raises_an_error_if_no_prompt_found(self, session):
        with pytest.raises(ModalNotFound):
            with session.dismiss_prompt():
                pass

    def test_dismisses_the_prompt_if_the_message_matches(self, session):
        with session.dismiss_prompt("Prompt opened"):
            session.click_link("Open prompt")
        assert session.has_xpath("//a[@id='open-prompt' and @response='dismissed']")

    def test_raises_error_if_the_message_does_not_match(self, session):
        with pytest.raises(ModalNotFound):
            with session.dismiss_prompt("Incorrect Text"):
                session.click_link("Open prompt")
