import pytest

import capybara
from capybara.tests.driver import Driver, build_driver_fixture


@capybara.register_driver("selenium_firefox")
def init_selenium_firefox_driver(app):
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

    from capybara.selenium.driver import Driver

    capabilities = DesiredCapabilities.FIREFOX.copy()
    capabilities["marionette"] = False

    return Driver(app, desired_capabilities=capabilities)


# Test the built-in drivers.
driver = build_driver_fixture(
    Driver("selenium_firefox"),
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
