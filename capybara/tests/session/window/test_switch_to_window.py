import pytest
from time import sleep

from capybara.exceptions import ScopeError, WindowError


@pytest.mark.requires("windows")
class SwitchToWindowTestCase:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_windows")
        assert session.has_css("body.loaded")

    @pytest.fixture
    def initial_window(self, session):
        return session.current_window

    @pytest.fixture(autouse=True)
    def teardown_windows(self, session, initial_window):
        try:
            yield
        finally:
            windows = set(session.windows) - set([initial_window])
            for window in windows:
                session.switch_to_window(window)
                window.close()
            session.switch_to_window(initial_window)


class TestSwitchToWindow(SwitchToWindowTestCase):
    def test_waits_for_window_to_appear(self, session):
        session.find("css", "#openWindowWithTimeout").click()
        session.switch_to_window(
            lambda: session.title == "Title of the first popup", wait=5)


class TestSwitchToWindowWithWindow(SwitchToWindowTestCase):
    def test_switches_to_a_window(self, session):
        window = session.open_new_window()
        assert session.title == "With Windows"
        session.switch_to_window(window)
        assert session.title in ["", "about:blank"]

    def test_raises_error_when_closed_window_is_passed(self, session):
        original_window = session.current_window
        new_window = session.open_new_window()
        session.switch_to_window(new_window)
        new_window.close()
        session.switch_to_window(original_window)
        with pytest.raises(session.driver.no_such_window_error):
            session.switch_to_window(new_window)


class TestSwitchToWindowWithLambda(SwitchToWindowTestCase):
    @pytest.fixture(autouse=True)
    def setup_windows(self, session):
        session.find("css", "#openTwoWindows").click()
        sleep(1)  # wait for the windows to open

    def test_switches_to_current_window(self, session):
        session.switch_to_window(lambda: session.title == "With Windows")
        assert session.has_css("#openTwoWindows")

    def test_finds_the_div_in_another_window(self, session):
        session.switch_to_window(lambda: session.title == "Title of popup two")
        assert session.has_css("#divInPopupTwo")

    def test_switches_multiple_times(self, session):
        session.switch_to_window(lambda: session.title == "Title of the first popup")
        assert session.has_css("#divInPopupOne")
        session.switch_to_window(lambda: session.title == "Title of popup two")
        assert session.has_css("#divInPopupTwo")

    def test_returns_the_window(self, session, initial_window):
        window = session.switch_to_window(lambda: session.title == "Title of popup two")
        assert window in set(session.windows) - set([initial_window])

    def test_raises_error_when_invoked_inside_a_scope(self, session):
        with pytest.raises(ScopeError) as excinfo:
            with session.scope("css", "#doesNotOpenWindows"):
                session.switch_to_window(lambda: session.title == "With Windows")
        assert "`switch_to_window` is not supposed to be invoked from within `scope`s, `frame`s, or other `window`s" in str(excinfo.value)

    def test_raises_error_when_invoked_inside_a_frame(self, session):
        with pytest.raises(ScopeError) as excinfo:
            with session.frame("frameOne"):
                session.switch_to_window(lambda: session.title == "With Windows")
        assert "`switch_to_window` is not supposed to be invoked from within `scope`s, `frame`s, or other `window`s" in str(excinfo.value)

    def test_raises_error_when_invoked_inside_a_window(self, session, initial_window):
        window = list(set(session.windows) - set([initial_window]))[0]
        with pytest.raises(ScopeError) as excinfo:
            with session.window(window):
                session.switch_to_window(lambda: session.title == "With Windows")
        assert "`switch_to_window` is not supposed to be invoked from within `scope`s, `frame`s, or other `window`s" in str(excinfo.value)

    def test_raises_error_if_window_matching_lambda_was_not_found(self, session):
        original = session.current_window
        with pytest.raises(WindowError) as excinfo:
            session.switch_to_window(lambda: session.title == "A title")
        assert "Could not find a window matching lambda" in str(excinfo.value)
        assert session.current_window == original

    def test_switches_to_original_window_if_error_is_raised_inside_block(self, session):
        original = session.switch_to_window(session.windows[1])
        with pytest.raises(RuntimeError) as excinfo:
            def failed_check():
                raise RuntimeError("error")
            session.switch_to_window(failed_check)
        assert "error" in str(excinfo.value)
        assert session.current_window == original
