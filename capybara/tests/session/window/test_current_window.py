import pytest

from capybara.window import Window


class TestCurrentWindow:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_windows")

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

    def test_returns_window(self, session):
        assert isinstance(session.current_window, Window)

    def test_modified_by_switching_to_another_window(self, session, initial_window):
        window = session.window_opened_by(
            lambda: session.find("css", "#openWindow").click())
        assert session.current_window == initial_window
        session.switch_to_window(window)
        assert session.current_window == window
