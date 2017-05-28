import capybara
from capybara.tests.suite import DriverSuite


@capybara.register_driver("selenium_firefox")
def init_selenium_firefox_driver(app):
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

    from capybara.selenium.driver import Driver

    capabilities = DesiredCapabilities.FIREFOX.copy()
    capabilities["marionette"] = False

    return Driver(app, desired_capabilities=capabilities)


SeleniumFirefoxDriverSuite = DriverSuite("selenium_firefox")
