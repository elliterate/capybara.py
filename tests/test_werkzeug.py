import capybara
from capybara.tests.suite import DriverSuite


@capybara.register_driver("werkzeug")
def init_werkzeug_driver(app):
    from capybara.werkzeug.driver import Driver

    return Driver(app)


WerkzeugDriverSuite = DriverSuite(
    "werkzeug",
    skip=["css", "frames", "hover", "js", "modals", "screenshot", "send_keys", "server", "windows"])
