import pytest


class TestTitle:
    def test_returns_the_title_of_the_page(self, session):
        session.visit("/with_title")
        assert session.title == "Test Title"

    @pytest.mark.requires("frames")
    def test_gets_the_title_of_the_top_level_browsing_context(self, session):
        session.visit("/within_frames")
        assert session.title == "With Frames"
        with session.frame("frameOne"):
            assert session.title == "With Frames"
