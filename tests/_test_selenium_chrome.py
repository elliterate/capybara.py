import os

import capybara
from capybara.tests.suite import DriverSuite


@capybara.register_driver("selenium_chrome")
def init_selenium_chrome_driver(app):
    from selenium.webdriver.chrome.options import Options

    from capybara.selenium.driver import Driver

    chrome_options = Options()
    if os.environ.get("CAPYBARA_CHROME_HEADLESS"):
        chrome_options.add_argument("--headless")

    return Driver(app, browser="chrome", chrome_options=chrome_options)


# See: https://bugs.chromium.org/p/chromedriver/issues/detail?id=1500
_skip = ["modals"]

# See: https://bugs.chromium.org/p/chromium/issues/detail?id=706008
if os.environ.get("CAPYBARA_CHROME_HEADLESS"):
    _skip.append("windows")

SeleniumChromeDriverSuite = DriverSuite("selenium_chrome", skip=_skip)
