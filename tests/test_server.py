from contextlib import closing
import pytest
import socket
from time import sleep

import capybara
from capybara.compat import urlopen
from capybara.server import Server
from capybara.utils import Counter, decode_bytes, encode_string


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
            return [encode_string("Hello Server!")]

        return app

    def test_spools_up_a_wsgi_server(self, app):
        server = Server(app).boot()
        with closing(urlopen("http://{}:{}".format(server.host, server.port))) as response:
            assert "Hello Server" in decode_bytes(response.read())

    def test_does_nothing_when_no_app_given(self):
        Server(None).boot()

    def test_binds_to_the_specified_port(self, app):
        capybara.server_host = "127.0.0.1"
        server = Server(app).boot()
        with closing(urlopen("http://127.0.0.1:{}".format(server.port))) as response:
            assert "Hello Server" in decode_bytes(response.read())

        capybara.server_host = "0.0.0.0"
        server = Server(app).boot()
        with closing(urlopen("http://127.0.0.1:{}".format(server.port))) as response:
            assert "Hello Server" in decode_bytes(response.read())

    def test_uses_specified_port(self, app):
        capybara.server_port = 22789
        server = Server(app).boot()
        with closing(urlopen("http://{}:22789".format(server.host))) as response:
            assert "Hello Server" in decode_bytes(response.read())

    def test_uses_given_port(self, app):
        server = Server(app, port=22790).boot()
        with closing(urlopen("http://{}:22790".format(server.host))) as response:
            assert "Hello Server" in decode_bytes(response.read())

    def test_finds_an_available_port(self, app):
        def app2(environ, start_response):
            start_response("200 OK", [])
            return [encode_string("Hello Second Server!")]

        server1 = Server(app).boot()
        server2 = Server(app2).boot()

        with closing(urlopen("http://{}:{}".format(server1.host, server1.port))) as response1:
            assert "Hello Server" in decode_bytes(response1.read())

        with closing(urlopen("http://{}:{}".format(server2.host, server2.port))) as response2:
            assert "Hello Second Server" in decode_bytes(response2.read())

    def test_uses_the_existing_server_if_it_is_already_running(self, app):
        server1 = Server(app).boot()
        server2 = Server(app).boot()

        with closing(urlopen("http://{}:{}".format(server1.host, server1.port))) as response1:
            assert "Hello Server" in decode_bytes(response1.read())

        with closing(urlopen("http://{}:{}".format(server2.host, server2.port))) as response2:
            assert "Hello Server" in decode_bytes(response2.read())

        assert server1.port == server2.port

    def test_waits_for_pending_requests(self):
        counter = Counter()

        def app(environ, start_response):
            with counter:
                sleep(0.2)
                start_response("200 OK", [])
                return [encode_string("Hello Server!")]

        server = Server(app).boot()

        # Start request, but don't wait for it to finish
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server.host, server.port))
        s.send(encode_string("GET / HTTP/1.0\r\n\r\n"))
        sleep(0.1)

        assert counter.value == 1

        server.wait_for_pending_requests()

        assert counter.value == 0

        s.close()
