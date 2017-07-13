from contextlib import closing
import pytest

import capybara
from capybara.compat import decode_socket_data, encode_socket_data, urlopen
from capybara.server import Server


class TestServer:
    @pytest.fixture(autouse=True)
    def teardown_settings(self):
        old_server_host = capybara.server_host
        old_server_port = capybara.server_port
        try:
            yield
        finally:
            capybara.server_host = old_server_host
            capybara.server_port = old_server_port

    @pytest.fixture
    def app(self):
        def app(environ, start_response):
            start_response("200 OK", [])
            return [encode_socket_data("Hello Server!")]

        return app

    def test_spools_up_a_wsgi_server(self, app):
        server = Server(app).boot()
        with closing(urlopen("http://{}:{}".format(server.host, server.port))) as response:
            assert "Hello Server" in decode_socket_data(response.read())

    def test_does_nothing_when_no_app_given(self):
        Server(None).boot()

    def test_binds_to_the_specified_port(self, app):
        capybara.server_host = "127.0.0.1"
        server = Server(app).boot()
        with closing(urlopen("http://127.0.0.1:{}".format(server.port))) as response:
            assert "Hello Server" in decode_socket_data(response.read())

        capybara.server_host = "0.0.0.0"
        server = Server(app).boot()
        with closing(urlopen("http://127.0.0.1:{}".format(server.port))) as response:
            assert "Hello Server" in decode_socket_data(response.read())

    def test_uses_specified_port(self, app):
        capybara.server_port = 22789
        server = Server(app).boot()
        with closing(urlopen("http://{}:22789".format(server.host))) as response:
            assert "Hello Server" in decode_socket_data(response.read())

    def test_uses_given_port(self, app):
        server = Server(app, port=22790).boot()
        with closing(urlopen("http://{}:22790".format(server.host))) as response:
            assert "Hello Server" in decode_socket_data(response.read())

    def test_finds_an_available_port(self, app):
        def app2(environ, start_response):
            start_response("200 OK", [])
            return [encode_socket_data("Hello Second Server!")]

        server1 = Server(app).boot()
        server2 = Server(app2).boot()

        with closing(urlopen("http://{}:{}".format(server1.host, server1.port))) as response1:
            assert "Hello Server" in decode_socket_data(response1.read())

        with closing(urlopen("http://{}:{}".format(server2.host, server2.port))) as response2:
            assert "Hello Second Server" in decode_socket_data(response2.read())

    def test_uses_the_existing_server_if_it_is_already_running(self, app):
        server1 = Server(app).boot()
        server2 = Server(app).boot()

        with closing(urlopen("http://{}:{}".format(server1.host, server1.port))) as response1:
            assert "Hello Server" in decode_socket_data(response1.read())

        with closing(urlopen("http://{}:{}".format(server2.host, server2.port))) as response2:
            assert "Hello Server" in decode_socket_data(response2.read())

        assert server1.port == server2.port
