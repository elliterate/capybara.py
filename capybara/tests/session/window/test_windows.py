import pytest

from capybara.window import Window

from capybara.tests.assertions import assert_windows_open


class TestWindows:
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

    def test_returns_window_instances(self, session):
        assert [isinstance(window, Window) for window in session.windows] == [True, True, True]

    def test_are_switchable(self, session):
        titles = []
        for window in session.windows:
            with session.window(window):
                titles.append(session.title)

        assert set(titles) == set(["With Windows", "Title of the first popup", "Title of popup two"])
