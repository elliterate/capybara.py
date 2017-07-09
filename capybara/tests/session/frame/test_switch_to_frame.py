import pytest

from capybara.exceptions import ScopeError


@pytest.mark.requires("frames")
class TestSwitchToFrame:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/within_frames")

    @pytest.fixture(autouse=True)
    def teardown_frames(self, session):
        try:
            yield
        finally:
            session.switch_to_frame("top")

    def test_finds_the_div_in_frame_one(self, session):
        frame = session.find("frame", "frameOne")
        session.switch_to_frame(frame)
        assert session.find("//*[@id='divInFrameOne']").text == "This is the text of divInFrameOne"

    def test_finds_the_div_in_frame_two(self, session):
        frame = session.find("frame", "frameTwo")
        session.switch_to_frame(frame)
        assert session.find("//*[@id='divInFrameTwo']").text == "This is the text of divInFrameTwo"

    def test_returns_to_the_parent_frame_when_told_to(self, session):
        frame = session.find("frame", "frameOne")
        session.switch_to_frame(frame)
        session.switch_to_frame("parent")
        assert session.find("//*[@id='divInMainWindow']").text == "This is the text for divInMainWindow"

    def test_is_able_to_switch_to_nested_frames(self, session):
        frame = session.find("frame", "parentFrame")
        session.switch_to_frame(frame)
        frame = session.find("frame", "childFrame")
        session.switch_to_frame(frame)
        frame = session.find("frame", "grandchildFrame1")
        session.switch_to_frame(frame)
        assert session.has_selector("css", "#divInFrameOne", text="This is the text of divInFrameOne")

    def test_resets_scope_when_changing_frames(self, session):
        frame = session.find("frame", "parentFrame")
        with session.scope("css", "#divInMainWindow"):
            session.switch_to_frame(frame)
            assert session.has_selector("css", "iframe#childFrame")
            session.switch_to_frame("parent")

    @pytest.mark.requires("js")
    def test_works_if_the_frame_is_closed(self, session):
        frame = session.find("frame", "parentFrame")
        session.switch_to_frame(frame)
        frame = session.find("frame", "childFrame")
        session.switch_to_frame(frame)

        session.click_link("Close Window")
        session.switch_to_frame("parent")  # Go back to parentFrame
        assert session.has_selector("css", "body#parentBody")
        assert session.has_no_selector("css", "#childFrame")
        session.switch_to_frame("parent")  # Go back to top

    def test_returns_to_the_top_frame(self, session):
        frame = session.find("frame", "parentFrame")
        session.switch_to_frame(frame)
        frame = session.find("frame", "childFrame")
        session.switch_to_frame(frame)
        session.switch_to_frame("top")
        assert session.find("//*[@id='divInMainWindow']").text == "This is the text for divInMainWindow"

    def test_raises_error_if_switching_to_parent_unmatched_inside_scope_as_its_nonsense(self, session):
        with pytest.raises(ScopeError) as excinfo:
            frame = session.find("frame", "parentFrame")
            session.switch_to_frame(frame)
            with session.scope("css", "#parentBody"):
                session.switch_to_frame("parent")
        assert "`switch_to_frame(\"parent\")` cannot be called " \
               "from inside a descendant frame's `scope` context." in str(excinfo.value)

    def test_raises_error_if_switching_to_top_inside_a_scope_in_a_frame_as_its_nonsense(self, session):
        with pytest.raises(ScopeError) as excinfo:
            frame = session.find("frame", "parentFrame")
            session.switch_to_frame(frame)
            with session.scope("css", "#parentBody"):
                session.switch_to_frame("top")
        assert "`switch_to_frame(\"top\")` cannot be called " \
               "from inside a descendant frame's `scope` context." in str(excinfo.value)

    def test_raises_error_if_switching_to_top_inside_a_nested_scope_in_a_frame_as_its_nonsense(self, session):
        frame = session.find("frame", "parentFrame")
        session.switch_to_frame(frame)
        with session.scope("css", "#parentBody"):
            session.switch_to_frame(session.find("frame", "childFrame"))
            with pytest.raises(ScopeError) as excinfo:
                session.switch_to_frame("top")
            assert "`switch_to_frame(\"top\")` cannot be called " \
                   "from inside a descendant frame's `scope` context." in str(excinfo.value)
            session.switch_to_frame("parent")
