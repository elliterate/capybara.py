import os
import pytest
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options

import capybara
from capybara.selenium.driver import Driver
from capybara.session import Session
from capybara.tests.app import app
from capybara.tests.suite import DriverSuite
from tests.selenium_session_test_case import SeleniumSessionTestCase


capabilities = DesiredCapabilities.FIREFOX.copy()
capabilities["marionette"] = True

firefox_options = Options()
if os.environ.get("HEADLESS"):
    firefox_options.add_argument("--headless")

# Allow the driver to attach files.
firefox_options.set_preference("dom.file.createInChild", True)


@capybara.register_driver("selenium_marionette")
def init_selenium_marionette_driver(app):
    return Driver(
        app,
        browser="firefox",
        desired_capabilities=capabilities,
        firefox_options=firefox_options)


@capybara.register_driver("selenium_marionette_clear_storage")
def init_selenium_marionette_clear_storage_driver(app):
    return Driver(
        app,
        browser="firefox",
        desired_capabilities=capabilities,
        clear_local_storage=True,
        clear_session_storage=True,
        firefox_options=firefox_options)


SeleniumMarionetteDriverSuite = DriverSuite("selenium_marionette")


class TestSeleniumSession(SeleniumSessionTestCase):
    @pytest.fixture(scope="module")
    def session(self):
        return Session("selenium_marionette", app)


class TestSeleniumMarionette:
    def test_reset_does_not_clear_either_storage_by_default(self):
        session = Session("selenium_marionette", app)
        session.visit("/with_js")
        session.find("css", "#set-storage").click()
        session.reset()
        session.visit("/with_js")
        assert session.evaluate_script("window.localStorage.length") > 0
        assert session.evaluate_script("window.sessionStorage.length") > 0

    def test_reset_clears_storage_when_set(self):
        session = Session("selenium_marionette_clear_storage", app)
        session.visit("/with_js")
        session.find("css", "#set-storage").click()
        session.reset()
        session.visit("/with_js")
        assert session.evaluate_script("window.localStorage.length") == 0
        assert session.evaluate_script("window.sessionStorage.length") == 0
