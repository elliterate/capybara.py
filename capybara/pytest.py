from __future__ import absolute_import

import pytest

import capybara
import capybara.dsl


def pytest_runtest_teardown():
    capybara.reset_sessions()


@pytest.fixture
def page():
    return capybara.dsl.page
