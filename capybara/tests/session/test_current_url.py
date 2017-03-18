from copy import copy
import pytest

import capybara
from capybara.server import Server
from capybara.tests.app import app


class TestCurrentURL:
    @pytest.fixture(scope="module")
    def servers(self):
        return [Server(copy(app)).boot() for _ in range(2)]

    @pytest.fixture
    def bases(self, servers):
        return ["http://{0}:{1}".format(s.host, s.port) for s in servers]

    @staticmethod
    def visit_host_links(session, bases):
        url = "{0}/host_links?absolute_host={1}".format(bases[0], bases[1])
        session.visit(url)

    @staticmethod
    def assert_on_server(session, server, path="/host", scheme="http"):
        url = "{0}://{1}:{2}{3}".format(scheme, server.host, server.port, path)
        host = "{0}://{1}".format(scheme, server.host)

        assert session.current_url.rstrip("?") == url
        assert session.current_host == host
        assert session.current_path == path

        if path == "/host":
            text = "Current host is {0}://{1}:{2}".format(scheme, server.host, server.port)
            assert session.has_text(text)

    def test_affected_by_visiting_a_page_directly(self, session, servers, bases):
        session.visit("{0}/host".format(bases[0]))
        self.assert_on_server(session, servers[0])

    def test_returns_to_the_app_host_when_visiting_a_relative_url(self, session, servers, bases):
        capybara.app_host = bases[1]

        session.visit("{0}/host".format(bases[0]))
        self.assert_on_server(session, servers[0])

        session.visit("/host")
        self.assert_on_server(session, servers[1])

        capybara.app_host = None

    def test_affected_by_setting_capybara_app_host(self, session, servers, bases):
        capybara.app_host = bases[0]
        session.visit("/host")
        self.assert_on_server(session, servers[0])

        capybara.app_host = bases[1]
        session.visit("/host")
        self.assert_on_server(session, servers[1])

        capybara.app_host = None

    def test_not_affected_by_following_a_relative_link(self, session, servers, bases):
        self.visit_host_links(session, bases)
        session.click_link("Relative Host")
        self.assert_on_server(session, servers[0])

    def test_affected_by_following_an_absolute_link(self, session, servers, bases):
        self.visit_host_links(session, bases)
        session.click_link("Absolute Host")
        self.assert_on_server(session, servers[1])

    def test_not_affected_by_posting_through_a_relative_form(self, session, servers, bases):
        self.visit_host_links(session, bases)
        session.click_button("Relative Host")
        self.assert_on_server(session, servers[0])

    def test_affected_by_posting_through_an_absolute_form(self, session, servers, bases):
        self.visit_host_links(session, bases)
        session.click_link("Absolute Host")
        self.assert_on_server(session, servers[1])

    def test_affected_by_following_a_redirect(self, session, servers, bases):
        session.visit("{0}/redirect".format(bases[0]))
        self.assert_on_server(session, servers[0], path="/landed")

    @pytest.mark.requires("js")
    def test_affected_by_push_state(self, session):
        session.visit("/with_js")
        session.execute_script("window.history.pushState({}, '', '/pushed')")
        assert session.current_path == "/pushed"

    @pytest.mark.requires("js")
    def test_affected_by_replace_state(self, session):
        session.visit("/with_js")
        session.execute_script("window.history.replaceState({}, '', '/replaced')")
        assert session.current_path == "/replaced"
