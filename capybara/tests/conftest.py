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
    original_enable_aria_label = capybara.enable_aria_label
    original_exact = capybara.exact
    original_ignore_hidden_elements = capybara.ignore_hidden_elements
    original_match = capybara.match
    original_raise_server_errors = capybara.raise_server_errors
    original_visible_text_only = capybara.visible_text_only
    original_wait_on_first_by_default = capybara.wait_on_first_by_default
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
        capybara.enable_aria_label = original_enable_aria_label
        capybara.exact = original_exact
        capybara.ignore_hidden_elements = original_ignore_hidden_elements
        capybara.match = original_match
        capybara.raise_server_errors = original_raise_server_errors
        capybara.visible_text_only = original_visible_text_only
        capybara.wait_on_first_by_default = original_wait_on_first_by_default


@pytest.fixture(scope="session")
def fixture_path():
    def fixture_path(fixture_name):
        return os.path.join(_FIXTURE_DIR, fixture_name)

    return fixture_path
