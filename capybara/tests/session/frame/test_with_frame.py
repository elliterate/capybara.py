import pytest

from capybara.exceptions import Ambiguous


@pytest.mark.requires("frames")
class TestWithFrame:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/within_frames")

    def test_finds_the_div_in_frame_one(self, session):
        with session.frame("frameOne"):
            assert session.find("//*[@id='divInFrameOne']").text == "This is the text of divInFrameOne"

    def test_finds_the_div_in_frame_two(self, session):
        with session.frame("frameTwo"):
            assert session.find("//*[@id='divInFrameTwo']").text == "This is the text of divInFrameTwo"

    def test_finds_the_text_div_in_the_main_window_after_finding_text_in_frame_one(self, session):
        with session.frame("frameOne"):
            assert session.find("//*[@id='divInFrameOne']").text == "This is the text of divInFrameOne"
        assert session.find("//*[@id='divInMainWindow']").text == "This is the text for divInMainWindow"

    def test_finds_the_text_div_in_the_main_window_after_finding_text_in_frame_two(self, session):
        with session.frame("frameTwo"):
            assert session.find("//*[@id='divInFrameTwo']").text == "This is the text of divInFrameTwo"
        assert session.find("//*[@id='divInMainWindow']").text == "This is the text for divInMainWindow"

    def test_finds_the_div_given_an_element(self, session):
        element = session.find("css", "#frameOne")
        with session.frame(element):
            assert session.find("//*[@id='divInFrameOne']").text == "This is the text of divInFrameOne"

    def test_finds_the_div_given_selector_and_locator(self, session):
        with session.frame("css", "#frameOne"):
            assert session.find("//*[@id='divInFrameOne']").text == "This is the text of divInFrameOne"

    def test_defaults_to_the_frame_selector_kind_when_only_options_passed(self, session):
        with session.frame(name="my frame one"):
            assert session.find("//*[@id='divInFrameOne']").text == "This is the text of divInFrameOne"

    def test_defaults_to_the_frame_selector_when_no_options_passed(self, session):
        container = session.find("css", "#divInMainWindow")
        with session.scope(container):
            # Ensure only one frame in scope
            with session.frame():
                assert session.has_css("body#parentBody")
        with pytest.raises(Ambiguous):
            # Multiple frames in scope here
            with session.frame():
                pass

    def test_finds_multiple_nested_frames(self, session):
        with session.frame("parentFrame"):
            with session.frame("childFrame"):
                with session.frame("grandchildFrame1"):
                    pass
                with session.frame("grandchildFrame2"):
                    pass

    def test_resets_scope_when_changing_frames(self, session):
        with session.scope("css", "#divInMainWindow"):
            with session.frame("innerParentFrame"):
                assert session.has_selector("css", "iframe#childFrame") is True

    def test_handles_a_frame_closing(self, session):
        with session.frame("parentFrame"):
            with session.frame("childFrame"):
                session.click_link("Close Window")
            assert session.has_selector("css", "body#parentBody")
            assert not session.has_selector("css", "#childFrame")
