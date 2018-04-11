import os

import capybara
from capybara.tests.suite import DriverSuite


@capybara.register_driver("selenium_ie")
def init_selenium_edgr_driver(app):
    from selenium.webdriver import DesiredCapabilities

    from capybara.selenium.driver import Driver

    capabilities = DesiredCapabilities.INTERNETEXPLORER.copy()
    capabilities['ensureCleanSession'] = True
    capabilities['ignoreProtectedModeSettings'] = True
    capabilities['forceCreateProcessApi'] = True
    capabilities['ensureCleanSession'] = True
    capabilities['ignoreZoomSetting'] = True
    capabilities['INTRODUCE_FLAKINESS_BY_IGNORING_SECURITY_DOMAINS'] = True

    return Driver(app, browser="ie", desired_capabilities=capabilities)


_skip = []

# See: https://bugs.chromium.org/p/chromium/issues/detail?id=706008
if os.environ.get("HEADLESS"):
    _skip.append("windows")

SeleniumIeDriverSuite = DriverSuite("selenium_ie", skip=_skip)
