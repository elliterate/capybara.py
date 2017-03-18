"""
Configuration for the :class:`Session` test suite.

This suite verifies the implementation of the :class:`Session` class, as well as those of one or
more drivers with which it is integrated during testing. The suite requires the declaration of a
parametrized ``driver`` fixture that declares the set of drivers to be tested::

    from capybara.tests.driver import Driver, build_driver_fixture

    driver = build_driver_fixture(
        Driver("driver_a", skip=["feature_a", "feature_b"]),
        Driver("driver_b", skip=["feature_c"]))
"""

import inspect
import os.path
import pytest

import capybara
from capybara.tests.app import app


_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
_FIXTURE_DIR = os.path.join(_DIR, "fixtures")


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    requires = item.get_marker("requires")
    if requires is not None:
        driver = item.callspec.params.get("driver")

        skipped_features = set(driver.skip)
        required_features = set(requires.args)

        missing_features = required_features & skipped_features
        if missing_features:
            pytest.skip("test requires {}".format(", ".join(sorted(list(missing_features)))))


@pytest.fixture(autouse=True)
def setup_capybara():
    original_app = capybara.app
    original_app_host = capybara.app_host
    original_automatic_reload = capybara.automatic_reload
    original_default_max_wait_time = capybara.default_max_wait_time
    original_default_selector = capybara.default_selector
    original_enable_aria_label = capybara.enable_aria_label
    original_exact = capybara.exact
    original_ignore_hidden_elements = capybara.ignore_hidden_elements
    original_match = capybara.match
    original_visible_text_only = capybara.visible_text_only
    original_wait_on_first_by_default = capybara.wait_on_first_by_default
    try:
        capybara.app = app
        capybara.app_host = None
        capybara.default_max_wait_time = 1
        capybara.default_selector = "xpath"
        yield
    finally:
        capybara.app = original_app
        capybara.app_host = original_app_host
        capybara.automatic_reload = original_automatic_reload
        capybara.default_max_wait_time = original_default_max_wait_time
        capybara.default_selector = original_default_selector
        capybara.enable_aria_label = original_enable_aria_label
        capybara.exact = original_exact
        capybara.ignore_hidden_elements = original_ignore_hidden_elements
        capybara.match = original_match
        capybara.visible_text_only = original_visible_text_only
        capybara.wait_on_first_by_default = original_wait_on_first_by_default


@pytest.fixture(scope="session")
def session(driver):
    from capybara.session import Session

    return Session(driver.name, app)


@pytest.fixture(scope="session")
def fixture_path():
    def fixture_path(fixture_name):
        return os.path.join(_FIXTURE_DIR, fixture_name)

    return fixture_path


@pytest.fixture(autouse=True)
def reset_session(session):
    try:
        yield
    finally:
        session.reset()
