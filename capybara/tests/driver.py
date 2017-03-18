import pytest


class Driver(object):
    """
    A driver to be tested.

    Args:
        name (str): The name of the driver.
        skip (List[str], optional): A list of features whose tests should be skipped because the
            driver does not support them. Defaults to [].
    """

    def __init__(self, name, skip=None):
        self.name = name
        self.skip = skip or []


def build_driver_fixture(*drivers):
    """
    Builds a parametrized ``driver`` fixture for testing.

    Args:
        *drivers (*Driver): One or more drivers to test.

    Returns:
        func: The driver fixture.
    """

    assert len(drivers) > 0, "at least one driver must be specified"

    @pytest.fixture(
        scope="session",
        params=drivers,
        ids=lambda d: d.name)
    def driver(request):
        return request.param

    return driver
