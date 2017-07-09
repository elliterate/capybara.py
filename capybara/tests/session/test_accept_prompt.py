import pytest

from capybara.exceptions import ModalNotFound


@pytest.mark.requires("modals")
class TestAcceptPrompt:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_js")

    def test_accepts_the_prompt_with_no_message(self, session):
        with session.accept_prompt():
            session.click_link("Open prompt")
        assert session.has_xpath("//a[@id='open-prompt' and @response='']")

    def test_raises_an_error_if_no_prompt_found(self, session):
        with pytest.raises(ModalNotFound):
            with session.accept_prompt():
                pass

    def test_accepts_the_prompt_with_a_response(self, session):
        with session.accept_prompt(response="the response"):
            session.click_link("Open prompt")
        assert session.has_xpath("//a[@id='open-prompt' and @response='the response']")

    def test_accepts_the_prompt_if_the_message_matches(self, session):
        with session.accept_prompt("Prompt opened", response="matched"):
            session.click_link("Open prompt")
        assert session.has_xpath("//a[@id='open-prompt' and @response='matched']")

    def test_raises_error_if_the_message_does_not_match(self, session):
        with pytest.raises(ModalNotFound):
            with session.accept_prompt("Incorrect Text", response="not matched"):
                session.click_link("Open prompt")
