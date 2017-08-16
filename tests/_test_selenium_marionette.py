import os

import capybara
from capybara.tests.suite import DriverSuite


@capybara.register_driver("selenium_marionette")
def init_selenium_marionette_driver(app):
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    from selenium.webdriver.firefox.options import Options

    from capybara.selenium.driver import Driver

    capabilities = DesiredCapabilities.FIREFOX.copy()
    capabilities["marionette"] = True

    firefox_options = Options()
    if os.environ.get("HEADLESS"):
        firefox_options.add_argument("--headless")

    # Allow the driver to attach files.
    firefox_options.set_preference("dom.file.createInChild", True)

    return Driver(
        app, browser="firefox", desired_capabilities=capabilities, firefox_options=firefox_options)


SeleniumMarionetteDriverSuite = DriverSuite("selenium_marionette")
