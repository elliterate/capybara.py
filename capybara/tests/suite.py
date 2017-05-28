from __future__ import absolute_import

import pytest

from capybara.tests.app import app


class DriverSuite(object):
    """
    Represents a suite of tests that should be run against a particular driver.

    Args:
        driver_name (str): The registered name of the driver to test.
        skip (List[str], optional): A list of features not supported by the driver. Tests in
            the suite marked as requiring these features will be skipped.
    """

    def __init__(self, driver_name, skip=None):
        self.driver_name = driver_name
        self.skip = skip or []

    @pytest.fixture(scope="session")
    def session(self):
        from capybara.session import Session

        return Session(self.driver_name, app)

    @pytest.fixture(autouse=True)
    def reset_session(self, session):
        try:
            yield
        finally:
            session.reset()
