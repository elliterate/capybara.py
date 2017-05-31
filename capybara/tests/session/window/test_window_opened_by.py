import pytest
from time import sleep

import capybara
from capybara.exceptions import WindowError
from capybara.window import Window

from capybara.tests.assertions import assert_windows_open


@pytest.mark.requires("windows")
class TestWindowOpenedBy:
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

    def test_raises_error_if_value_of_wait_is_less_than_timeout(self, session):
        button = session.find("css", "#openWindowWithLongerTimeout")
        with capybara.using_wait_time(2):
            with pytest.raises(WindowError):
                session.window_opened_by(lambda: button.click(), wait=0.8)
        assert_windows_open(session, 2)

    def test_finds_window_if_value_of_wait_is_more_than_timeout(self, session):
        button = session.find("css", "#openWindowWithTimeout")
        with capybara.using_wait_time(0.1):
            window = session.window_opened_by(lambda: button.click(), wait=1.5)
        assert isinstance(window, Window)

    def test_raises_error_if_default_max_wait_time_is_less_than_timeout(self, session):
        button = session.find("css", "#openWindowWithLongerTimeout")
        with capybara.using_wait_time(0.4):
            with pytest.raises(WindowError):
                session.window_opened_by(lambda: button.click())
        assert_windows_open(session, 2)

    def test_finds_window_if_default_max_wait_time_is_more_than_timeout(self, session):
        button = session.find("css", "#openWindowWithTimeout")
        with capybara.using_wait_time(1.5):
            window = session.window_opened_by(lambda: button.click())
        assert isinstance(window, Window)

    def test_raises_error_when_two_windows_have_been_opened_by_lambda(self, session):
        button = session.find("css", "#openTwoWindows")
        with pytest.raises(WindowError):
            # It's possible for ``window_opened_by`` to be fulfilled before the second
            # window opens.
            session.window_opened_by(lambda: button.click() or sleep(1))
        assert_windows_open(session, 3)

    def test_raises_error_when_no_windows_were_opened_by_lambda(self, session):
        button = session.find("css", "#doesNotOpenWindows")
        with pytest.raises(WindowError):
            session.window_opened_by(lambda: button.click())
