import pytest


class WindowTestCase:
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


class TestWindowClose(WindowTestCase):
    @pytest.fixture
    def other_window(self, session):
        return session.window_opened_by(
            lambda: session.find("css", "#openWindow").click())

    def test_switches_to_original_window_if_invoked_not_for_current_window(self, session, initial_window, other_window):
        assert len(session.windows) == 2
        assert session.current_window == initial_window
        other_window.close()
        assert len(session.windows) == 1
        assert session.current_window == initial_window
