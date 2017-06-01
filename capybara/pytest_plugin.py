import pytest

import capybara
import capybara.dsl


def pytest_runtest_setup(item):
    if item.get_marker("js"):
        capybara.current_driver = capybara.javascript_driver

    driver = item.get_marker("driver")
    if driver:
        assert len(driver.args) == 1, "exactly one driver must be specified"
        capybara.current_driver = driver.args[0]


def pytest_runtest_teardown():
    capybara.reset_sessions()
    capybara.use_default_driver()


@pytest.fixture
def page():
    return capybara.dsl.page
