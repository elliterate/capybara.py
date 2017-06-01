import capybara
from capybara.tests.suite import DriverSuite


@capybara.register_driver("selenium_chrome")
def init_selenium_chrome_driver(app):
    from capybara.selenium.driver import Driver

    return Driver(app, browser="chrome")


SeleniumChromeDriverSuite = DriverSuite(
    "selenium_chrome",

    # See: https://bugs.chromium.org/p/chromedriver/issues/detail?id=1500
    skip=["modals"])
