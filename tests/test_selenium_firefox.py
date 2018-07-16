import pytest
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import capybara
from capybara.session import Session
from capybara.selenium.driver import Driver
from capybara.tests.app import app
from capybara.tests.suite import DriverSuite
from tests.selenium_session_test_case import SeleniumSessionTestCase


capabilities = DesiredCapabilities.FIREFOX.copy()
capabilities["marionette"] = False


@capybara.register_driver("selenium_firefox")
def init_selenium_firefox_driver(app):
    return Driver(
        app,
        browser="firefox",
        desired_capabilities=capabilities)


@capybara.register_driver("selenium_firefox_clear_storage")
def init_selenium_firefox_clear_storage_driver(app):
    return Driver(
        app,
        browser="firefox",
        clear_local_storage=True,
        clear_session_storage=True,
        desired_capabilities=capabilities)


SeleniumFirefoxDriverSuite = DriverSuite("selenium_firefox", skip=["fullscreen"])


class TestSeleniumSession(SeleniumSessionTestCase):
    @pytest.fixture(scope="module")
    def session(self):
        return Session("selenium_firefox", app)


class TestSeleniumFirefox:
    def test_reset_does_not_clear_either_storage_by_default(self):
        session = Session("selenium_firefox", app)
        session.visit("/with_js")
        session.find("css", "#set-storage").click()
        session.reset()
        session.visit("/with_js")
        assert session.evaluate_script("window.localStorage.length") > 0
        assert session.evaluate_script("window.sessionStorage.length") > 0

    def test_reset_clears_storage_when_set(self):
        session = Session("selenium_firefox_clear_storage", app)
        session.visit("/with_js")
        session.find("css", "#set-storage").click()
        session.reset()
        session.visit("/with_js")
        assert session.evaluate_script("window.localStorage.length") == 0
        assert session.evaluate_script("window.sessionStorage.length") == 0
