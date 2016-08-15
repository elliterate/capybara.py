import pytest

from capybara.exceptions import ScopeError, WindowError

from capybara.tests.assertions import assert_windows_open


class TestWithWindow:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_windows")
        session.find("css", "#openTwoWindows").click()
        assert_windows_open(session, 3)

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

    def test_switches_to_another_window(self, session, initial_window):
        window = list(set(session.windows) - set([initial_window]))[0]
        with session.window(window):
            assert session.title in ["Title of the first popup", "Title of popup two"]
        assert session.title == "With Windows"

    def test_switches_back_if_exception_was_raised(self, session, initial_window):
        window = list(set(session.windows) - set([initial_window]))[0]
        with pytest.raises(RuntimeError) as excinfo:
            with session.window(window):
                raise RuntimeError("some error")
        assert "some error" in str(excinfo.value)
        assert session.current_window == initial_window
        assert session.has_css("#doesNotOpenWindows")

    def test_raises_error_if_called_within_a_scope(self, session, initial_window):
        window = list(set(session.windows) - set([initial_window]))[0]
        with pytest.raises(ScopeError):
            with session.scope("html"):
                with session.window(window):
                    pass
        assert session.current_window == initial_window
        assert session.has_css("#doesNotOpenWindows")

    def test_finds_the_matching_lambda_in_another_window(self, session):
        with session.window(lambda: session.title == "Title of the first popup"):
            assert session.has_css("#divInPopupOne")

    def test_finds_the_matching_lambda_in_both_windows(self, session):
        with session.window(lambda: session.title == "Title of popup two"):
            assert session.has_css("#divInPopupTwo")
        with session.window(lambda: session.title == "Title of the first popup"):
            assert session.has_css("#divInPopupOne")
        assert session.title == "With Windows"

    def test_raises_error_if_lambda_was_not_matched(self, session, initial_window):
        with pytest.raises(WindowError) as excinfo:
            with session.window(lambda: session.title == "Invalid title"):
                pass
        assert "Could not find a window matching lambda" in str(excinfo.value)
        assert session.current_window == initial_window
        assert session.has_css("#doesNotOpenWindows")

    def test_switches_back_if_exception_was_raised_inside_window_matched_with_lambda(self, session, initial_window):
        with pytest.raises(RuntimeError) as excinfo:
            with session.window(lambda: session.title == "Title of popup two"):
                raise RuntimeError("some error")
        assert "some error" in str(excinfo.value)
        assert session.current_window == initial_window
