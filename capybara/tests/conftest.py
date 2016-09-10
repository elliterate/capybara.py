import inspect
import os.path
import pytest

import capybara
from capybara.tests.app import app


_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
_FIXTURE_DIR = os.path.join(_DIR, "fixtures")


@pytest.fixture(autouse=True)
def setup_capybara():
    original_app = capybara.app
    original_app_host = capybara.app_host
    original_automatic_reload = capybara.automatic_reload
    original_default_max_wait_time = capybara.default_max_wait_time
    original_default_selector = capybara.default_selector
    original_exact = capybara.exact
    original_ignore_hidden_elements = capybara.ignore_hidden_elements
    original_visible_text_only = capybara.visible_text_only
    try:
        capybara.app = app
        capybara.app_host = None
        capybara.default_max_wait_time = 1
        capybara.default_selector = "xpath"
        yield
    finally:
        capybara.app = original_app
        capybara.app_host = original_app_host
        capybara.automatic_reload = original_automatic_reload
        capybara.default_max_wait_time = original_default_max_wait_time
        capybara.default_selector = original_default_selector
        capybara.exact = original_exact
        capybara.ignore_hidden_elements = original_ignore_hidden_elements
        capybara.visible_text_only = original_visible_text_only


@pytest.fixture(scope="session")
def session(driver):
    from capybara.session import Session

    return Session(driver, app)


@pytest.fixture(scope="session")
def fixture_path():
    def fixture_path(fixture_name):
        return os.path.join(_FIXTURE_DIR, fixture_name)

    return fixture_path


@pytest.fixture(autouse=True)
def reset_session(session):
    try:
        yield
    finally:
        session.reset()
