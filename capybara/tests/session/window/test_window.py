from flaky import flaky
import pytest
from time import sleep


@pytest.mark.requires("windows")
class WindowTestCase:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_windows")

    @pytest.fixture
    def initial_window(self, session):
        return session.current_window

    @pytest.fixture
    def other_window(self, session):
        return session.window_opened_by(
            lambda: session.find("css", "#openWindow").click())

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


class TestWindowExists(WindowTestCase):
    def test_becomes_false_after_window_was_closed(self, session, other_window):
        assert other_window.exists is True
        session.switch_to_window(other_window)
        other_window.close()
        assert other_window.exists is False


class TestWindowClosed(WindowTestCase):
    def test_becomes_true_after_window_was_closed(self, session, other_window):
        assert other_window.closed is False
        session.switch_to_window(other_window)
        other_window.close()
        assert other_window.closed is True


class TestWindowCurrent(WindowTestCase):
    def test_becomes_true_after_switching_to_window(self, session, other_window):
        assert other_window.current is False
        session.switch_to_window(other_window)
        assert other_window.current is True

    def test_returns_false_if_window_is_closed(self, session, other_window):
        session.switch_to_window(other_window)
        other_window.close()
        assert other_window.current is False


class TestWindowClose(WindowTestCase):
    def test_switches_to_original_window_if_invoked_not_for_current_window(self, session, initial_window, other_window):
        assert len(session.windows) == 2
        assert session.current_window == initial_window
        other_window.close()
        assert len(session.windows) == 1
        assert session.current_window == initial_window


class TestWindowSize(WindowTestCase):
    @staticmethod
    def win_size(session):
        return session.evaluate_script(
            "[window.outerWidth || window.innerWidth, window.outerHeight || window.innerHeight]")

    def test_returns_size_of_whole_window(self, session):
        assert session.current_window.size == self.win_size(session)

    @flaky
    def test_switches_to_original_window_if_invoked_not_for_current_window(self, session, initial_window, other_window):
        sleep(1)  # wait for ``other_window`` to finish opening
        with session.window(other_window):
            size = self.win_size(session)
        assert other_window.size == size
        assert session.current_window == initial_window


class TestWindowResizeTo(WindowTestCase):
    def test_is_able_to_resize_window(self, session):
        width, height = session.current_window.size
        session.current_window.resize_to(width - 100, height - 100)
        sleep(1)
        assert session.current_window.size == [width - 100, height - 100]

    def test_stays_on_current_window_if_invoked_not_for_current_window(self, session, initial_window, other_window):
        other_window.resize_to(400, 300)
        assert session.current_window == initial_window

        with session.window(other_window):
            assert session.current_window.size == [400, 300]


class TestWindowMaximize(WindowTestCase):
    def test_is_able_to_maximize_window(self, session):
        start_width, start_height = 400, 300
        session.current_window.resize_to(start_width, start_height)
        sleep(0.5)

        session.current_window.maximize()
        sleep(0.5)

        max_width, max_height = session.current_window.size

        assert max_width > start_width
        assert max_height > start_height

    def test_stays_on_current_window_if_invoked_not_for_current_window(self, session, initial_window, other_window):
        cur_window_size = session.current_window.size

        other_window.resize_to(400, 300)
        sleep(0.5)
        other_window.maximize()
        sleep(0.5)

        assert session.current_window == initial_window
        assert session.current_window.size == cur_window_size

        ow_width, ow_height = other_window.size

        assert ow_width > 400
        assert ow_height > 300


@pytest.mark.requires("fullscreen")
class TestWindowFullscreen(WindowTestCase):
    @pytest.fixture(autouse=True)
    def restore_window(self, session):
        initial_size = session.current_window.size
        try:
            yield
        finally:
            session.current_window.resize_to(*initial_size)

    def test_fullscreens_the_window(self, session):
        session.current_window.fullscreen()
