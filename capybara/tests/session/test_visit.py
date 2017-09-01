import pytest
import re

import capybara
from capybara.compat import urlparse
from capybara.session import Session
from capybara.tests.app import AppError


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

    @pytest.mark.requires("server")
    def test_raises_any_errors_caught_inside_the_server(self, session):
        session.visit("/error")
        with pytest.raises(AppError):
            session.visit("/")

    def test_sends_no_referrer_when_visiting_a_page(self, session):
        session.visit("/get_referrer")
        assert session.has_text("No referrer")

    def test_sends_no_referrer_when_visiting_a_second_page(self, session):
        session.visit("/get_referrer")
        session.visit("/get_referrer")
        assert session.has_text("No referrer")

    def test_sends_a_referrer_when_following_a_link(self, session):
        session.visit("/referrer_base")
        session.find("//a[@href='/get_referrer']").click()
        assert session.has_text(re.compile(r"http://.*/referrer_base"))

    def test_preserves_the_original_referrer_url_when_following_a_redirect(self, session):
        session.visit("/referrer_base")
        session.find("//a[@href='/redirect_to_get_referrer']").click()
        assert session.has_text(re.compile(r"http://.*/referrer_base"))

    def test_sends_a_referrer_when_submitting_a_form(self, session):
        session.visit("/referrer_base")
        session.find("//input").click()
        assert session.has_text(re.compile(r"http://.*/referrer_base"))

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
