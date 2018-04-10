import os

import capybara
from capybara.tests.suite import DriverSuite


@capybara.register_driver("selenium_edge")
def init_selenium_edgr_driver(app):
    from capybara.selenium.driver import Driver

    return Driver(app, browser="edge")


_skip = []

# See: https://bugs.chromium.org/p/chromium/issues/detail?id=706008
if os.environ.get("HEADLESS"):
    _skip.append("windows")

SeleniumEdgeDriverSuite = DriverSuite("selenium_edge", skip=_skip)
