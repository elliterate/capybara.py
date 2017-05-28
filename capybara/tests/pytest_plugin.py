import inspect
import os.path
import pytest

from capybara.tests.collector import GraftedSubSession
from capybara.tests.suite import DriverSuite


_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def pytest_pycollect_makeitem(collector, name, obj):
    if isinstance(obj, DriverSuite):
        return Driver(obj, parent=collector)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    # See if this test ``requires`` any special driver features.
    requires = item.get_marker("requires")
    if requires is not None:
        driver = item.getparent(Driver).obj

        skipped_features = set(driver.skip)
        required_features = set(requires.args)

        # Verify that the driver under test supports the required features.
        missing_features = required_features & skipped_features
        if missing_features:
            pytest.skip("test requires {}".format(", ".join(sorted(list(missing_features)))))


class Driver(GraftedSubSession):
    """
    A pytest collector for the driver test suite.

    Args:
        suite (DriverSuite): The user-defined suite for testing their driver.
        parent (Collector): The parent pytest collector.
    """

    def __init__(self, suite, parent):
        self.suite = suite

        super(Driver, self).__init__(self.suite.driver_name, parent, _DIR)

    @property
    def obj(self):
        """
        The collected object.

        This is used (and thus required) by pytest for various things, including (most notably,
        for our purposes) fixture factory collection.
        """
        return self.suite
