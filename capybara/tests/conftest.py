import pytest

import capybara
from capybara.tests.app import app


@pytest.fixture(autouse=True)
def setup_capybara():
    original_app = capybara.app
    original_app_host = capybara.app_host
    try:
        capybara.app = app
        capybara.app_host = None
        yield
    finally:
        capybara.app = original_app
        capybara.app_host = original_app_host


@pytest.fixture(scope="session")
def session(driver):
    from capybara.session import Session

    return Session(driver, app)
