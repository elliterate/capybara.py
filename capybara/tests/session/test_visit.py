import pytest

import capybara
from capybara.compat import urlparse
from capybara.session import Session


class TestVisit:
    def test_fetches_a_response_from_the_driver_with_a_relative_url(self, session):
        session.visit("/")
        assert session.has_text("Hello world!")
        session.visit("/foo")
        assert session.has_text("Another World")

    def test_fetches_a_response_from_the_driver_with_an_absolute_url_with_a_port(self, session):
        # Preparation
        session.visit("/")
        root_uri = urlparse(session.current_url)

        session.visit("http://{}/".format(root_uri.netloc))
        assert session.has_text("Hello world!")
        session.visit("http://{}/foo".format(root_uri.netloc))
        assert session.has_text("Another World")

    def test_fetches_a_response_when_absolute_uri_does_not_have_a_trailing_slash(self, session):
        # Preparation
        session.visit("/")
        root_uri = urlparse(session.current_url)

        session.visit("http://{}".format(root_uri.netloc))
        assert session.has_text("Hello world!")

    def test_sets_cookie_if_a_blank_path_is_specified(self, session):
        session.visit("")
        session.visit("/get_cookie")
        assert session.has_text("root cookie")


class TestVisitWithoutApp:
    def test_does_not_instantiate_a_server(self, session):
        serverless_session = Session(session.mode, None)
        assert serverless_session.server is None

    @pytest.mark.requires("server")
    def test_respects_app_host(self, session):
        serverless_session = Session(session.mode, None)
        capybara.app_host = "http://{}:{}".format(session.server.host, session.server.port)
        serverless_session.visit("/foo")
        assert serverless_session.has_text("Another World")

    @pytest.mark.requires("server")
    def test_visits_a_fully_qualified_url(self, session):
        serverless_session = Session(session.mode, None)
        serverless_session.visit(
            "http://{}:{}/foo".format(session.server.host, session.server.port))
        assert serverless_session.has_text("Another World")
