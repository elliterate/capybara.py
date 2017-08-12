import capybara
from capybara.tests.suite import DriverSuite


@capybara.register_driver("selenium_marionette")
def init_selenium_marionette_driver(app):
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

    from capybara.selenium.driver import Driver

    capabilities = DesiredCapabilities.FIREFOX.copy()
    capabilities["marionette"] = True

    return Driver(app, browser="firefox", desired_capabilities=capabilities)


SeleniumMarionetteDriverSuite = DriverSuite("selenium_marionette")
