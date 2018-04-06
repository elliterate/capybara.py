import pytest


@pytest.mark.requires("frames")
class TestFrameURL:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/within_frames")

    def test_returns_the_url_in_a_frame(self, session):
        with session.frame("frameOne"):
            assert session.driver.frame_url.endswith("/frame_one")

    def test_returns_the_url_in_frame_two(self, session):
        with session.frame("frameTwo"):
            assert session.driver.frame_url.endswith("/frame_two")

    def test_returns_the_url_in_the_main_frame(self, session):
        assert session.driver.frame_url.endswith("/within_frames")
