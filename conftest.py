import pytest

import capybara
from capybara.tests.driver import Driver, build_driver_fixture


# Test the built-in drivers.
driver = build_driver_fixture(
    Driver("selenium"),
    Driver("werkzeug", skip=[
        "frames", "hover", "js", "modals", "screenshot", "send_keys", "server", "windows"]))


@pytest.fixture(autouse=True)
def setup_capybara():
    original_default_selector = capybara.default_selector
    try:
        capybara.default_selector = "xpath"
        yield
    finally:
        capybara.default_selector = original_default_selector
