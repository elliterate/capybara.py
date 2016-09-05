import pytest

import capybara


@pytest.fixture(scope="session", params=["selenium"])
def driver(request):
    return request.param


@pytest.fixture(autouse=True)
def setup_capybara():
    original_default_selector = capybara.default_selector
    try:
        capybara.default_selector = "xpath"
        yield
    finally:
        capybara.default_selector = original_default_selector
