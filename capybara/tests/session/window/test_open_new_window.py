import pytest


class TestOpenNewWindow:
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

    def test_opens_new_window_with_blank_url_and_title(self, session):
        window = session.open_new_window()
        session.switch_to_window(window)
        assert session.title in ["", "about:blank"]
        assert session.current_url == "about:blank"

    def test_opens_window_with_changeable_content(self, session):
        window = session.open_new_window()
        with session.window(window):
            session.visit("/with_html")
            assert session.has_css("#first")
