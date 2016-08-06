import pytest

import capybara


class DSLTestCase:
    @pytest.fixture(autouse=True)
    def teardown_capybara(self):
        original_app = capybara.app
        try:
            yield
        finally:
            capybara.app = original_app


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
