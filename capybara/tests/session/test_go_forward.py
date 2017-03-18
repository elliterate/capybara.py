import pytest


@pytest.mark.requires("js")
class TestGoForward:
    def test_fetches_a_response_from_the_driver_for_the_next_page(self, session):
        session.visit("/")
        assert session.has_text("Hello world!")
        session.visit("/foo")
        assert session.has_text("Another World")
        session.go_back()
        assert session.has_text("Hello world!")
        session.go_forward()
        assert session.has_text("Another World")
