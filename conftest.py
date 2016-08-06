import pytest


@pytest.fixture(scope="session", params=["selenium"])
def driver(request):
    return request.param
