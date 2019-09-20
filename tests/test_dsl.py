import pytest

import capybara


class DSLTestCase:
    @pytest.fixture(autouse=True)
    def teardown_capybara(self):
        original_app = capybara.app
        original_current_driver = capybara.current_driver
        original_default_max_wait_time = capybara.default_max_wait_time
        original_session_name = capybara.session_name
        try:
            yield
        finally:
            capybara.app = original_app
            capybara.current_driver = original_current_driver
            capybara.default_max_wait_time = original_default_max_wait_time
            capybara.session_name = original_session_name


class TestUseDefaultDriver(DSLTestCase):
    def test_restores_the_default_driver(self):
        capybara.current_driver = "selenium"
        capybara.use_default_driver()
        assert capybara.current_driver is None


class TestUsingDriver(DSLTestCase):
    def test_sets_the_driver_using_current_driver(self):
        with capybara.using_driver("selenium"):
            assert capybara.current_driver == "selenium"

    def test_resets_the_driver(self):
        with capybara.using_driver("selenium"):
            pass
        assert capybara.current_driver is None

    def test_resets_the_driver_even_if_an_exception_occurs(self):
        with pytest.raises(RuntimeError):
            with capybara.using_driver("selenium"):
                raise RuntimeError("ohnoes!")
        assert capybara.current_driver is None

    def test_returns_the_driver_to_what_it_was_previously(self):
        capybara.current_driver = "selenium"
        with capybara.using_driver("webtest"):
            with capybara.using_driver("werkzeug"):
                assert capybara.current_driver == "werkzeug"
            assert capybara.current_driver == "webtest"
        assert capybara.current_driver == "selenium"


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

    def test_changes_with_the_current_driver(self):
        assert capybara.current_session().mode == "werkzeug"
        capybara.current_driver = "selenium"
        assert capybara.current_session().mode == "selenium"

    def test_persists_event_across_driver_changes(self):
        object_id = id(capybara.current_session())
        assert id(capybara.current_session()) == object_id

        capybara.current_driver = "selenium"
        assert capybara.current_session().mode == "selenium"
        assert id(capybara.current_session()) != object_id

        capybara.current_driver = "werkzeug"
        assert id(capybara.current_session()) == object_id

    def test_changes_when_changing_the_application(self):
        object_id = id(capybara.current_session())
        assert id(capybara.current_session()) == object_id
        capybara.app = lambda: None
        assert id(capybara.current_session()) != object_id
        assert capybara.current_session().app == capybara.app

    def test_changes_when_the_session_name_changes(self):
        object_id = id(capybara.current_session())
        capybara.session_name = "administrator"
        assert capybara.session_name == "administrator"
        assert id(capybara.current_session()) != object_id
        capybara.session_name = "default"
        assert capybara.session_name == "default"
        assert id(capybara.current_session()) == object_id


class TestUsingSession(DSLTestCase):
    def test_changes_the_session_name_for_the_duration_of_the_block(self):
        assert capybara.session_name == "default"
        with capybara.using_session("administrator"):
            assert capybara.session_name == "administrator"
        assert capybara.session_name == "default"

    def test_resets_the_session_to_the_default_even_if_an_exception_occurs(self):
        try:
            with capybara.using_session("raise"):
                raise RuntimeError()
        except RuntimeError:
            pass
        assert capybara.session_name == "default"

    def test_is_nestable(self):
        with capybara.using_session("outer"):
            assert capybara.session_name == "outer"
            with capybara.using_session("inner"):
                assert capybara.session_name == "inner"
            assert capybara.session_name == "outer"
        assert capybara.session_name == "default"


class TestSessionName(DSLTestCase):
    def test_defaults_to_default(self):
        assert capybara.session_name == "default"


class TestUsingDSLMixin(DSLTestCase):
    @pytest.fixture
    def myclass(self):
        from capybara.dsl import DSLMixin
        class MyClass(DSLMixin):
            pass
        return MyClass()

    def test_uses_current_session(self, myclass):
        assert myclass.has_no_current_path("/")
