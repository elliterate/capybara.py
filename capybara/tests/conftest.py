import pytest

import capybara
from capybara.tests.app import app


@pytest.fixture(autouse=True)
def setup_capybara():
    original_app = capybara.app
    original_app_host = capybara.app_host
    original_default_max_wait_time = capybara.default_max_wait_time
    try:
        capybara.app = app
        capybara.app_host = None
        capybara.default_max_wait_time = 1
        yield
    finally:
        capybara.app = original_app
        capybara.app_host = original_app_host
        capybara.default_max_wait_time = original_default_max_wait_time


@pytest.fixture(scope="session")
def session(driver):
    from capybara.session import Session

    return Session(driver, app)
