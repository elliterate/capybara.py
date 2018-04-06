import pytest


@pytest.mark.requires("frames")
class TestFrameTitle:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/within_frames")

    def test_returns_the_title_in_a_frame(self, session):
        with session.frame("frameOne"):
            assert session.driver.frame_title == "This is the title of frame one"

    def test_returns_the_title_in_frame_two(self, session):
        with session.frame("frameTwo"):
            assert session.driver.frame_title == "This is the title of frame two"

    def test_returns_the_title_in_the_main_frame(self, session):
        assert session.driver.frame_title == "With Frames"
