import pytest

import capybara


class DSLTestCase:
    @pytest.fixture(autouse=True)
    def teardown_capybara(self):
        original_app = capybara.app
        original_default_max_wait_time = capybara.default_max_wait_time
        try:
            yield
        finally:
            capybara.app = original_app
            capybara.default_max_wait_time = original_default_max_wait_time


class TestUsingWaitTime(DSLTestCase):
    def test_switches_and_restores_the_wait_time(self):
        previous_wait_time = capybara.default_max_wait_time
        with capybara.using_wait_time(6):
            in_context = capybara.default_max_wait_time
        assert in_context == 6
        assert capybara.default_max_wait_time == previous_wait_time

    def test_ensures_wait_time_is_reset(self):
        previous_wait_time = capybara.default_max_wait_time
        with pytest.raises(RuntimeError) as excinfo:
            with capybara.using_wait_time(6):
                raise RuntimeError("hell")
        assert "hell" in str(excinfo.value)
        assert capybara.default_max_wait_time == previous_wait_time


class TestApp(DSLTestCase):
    def test_is_changeable(self):
        capybara.app = "foobar"
        assert capybara.app == "foobar"


class TestCurrentSession(DSLTestCase):
    def test_uses_app_as_the_application(self):
        capybara.app = lambda: None
        assert capybara.current_session().app == capybara.app

    def test_changes_when_changing_the_application(self):
        object_id = id(capybara.current_session())
        assert id(capybara.current_session()) == object_id
        capybara.app = lambda: None
        assert id(capybara.current_session()) != object_id
        assert capybara.current_session().app == capybara.app
