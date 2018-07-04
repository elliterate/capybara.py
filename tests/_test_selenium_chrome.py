import os
from selenium.webdriver.chrome.options import Options

import capybara
from capybara.session import Session
from capybara.selenium.driver import Driver
from capybara.tests.app import app
from capybara.tests.suite import DriverSuite


chrome_options = Options()
if os.environ.get("HEADLESS"):
    chrome_options.add_argument("--headless")


@capybara.register_driver("selenium_chrome")
def init_selenium_chrome_driver(app):
    return Driver(
        app,
        browser="chrome",
        chrome_options=chrome_options)


@capybara.register_driver("selenium_chrome_clear_storage")
def init_selenium_chrome_driver(app):
    return Driver(
        app,
        browser="chrome",
        clear_local_storage=True,
        clear_session_storage=True,
        chrome_options=chrome_options)


# See: https://bugs.chromium.org/p/chromedriver/issues/detail?id=1500
_skip = ["modals"]

# See: https://bugs.chromium.org/p/chromium/issues/detail?id=706008
if os.environ.get("HEADLESS"):
    _skip.append("windows")

SeleniumChromeDriverSuite = DriverSuite("selenium_chrome", skip=_skip)


class TestSeleniumChrome:
    def test_reset_does_not_clear_either_storage_by_default(self):
        session = Session("selenium_chrome", app)
        session.visit("/with_js")
        session.find("css", "#set-storage").click()
        session.reset()
        session.visit("/with_js")
        assert session.evaluate_script("window.localStorage.length") > 0
        assert session.evaluate_script("window.sessionStorage.length") > 0

    def test_reset_clears_storage_when_set(self):
        session = Session("selenium_chrome_clear_storage", app)
        session.visit("/with_js")
        session.find("css", "#set-storage").click()
        session.reset()
        session.visit("/with_js")
        assert session.evaluate_script("window.localStorage.length") == 0
        assert session.evaluate_script("window.sessionStorage.length") == 0
