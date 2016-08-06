from contextlib import closing
import sys
from threading import Thread
if sys.version_info >= (3, 0):
    from urllib.error import URLError
    from urllib.request import urlopen
else:
    from urllib2 import URLError, urlopen

import capybara
from capybara.utils import cached_property, find_available_port, timeout


class Server(object):
    """
    Serves a WSGI-compliant app for Capybara to test.

    Args:
        app (object): The WSGI-compliant app to serve.
        port (int, optional): The port on which the server should be available.
            Defaults to :data:`capybara.server_port`, or the last port used by the
            given app, or a random available port.
        host (str, optional): The host on which the server should be available.
            Defaults to :data:`capybara.server_host`.
    """

    _ports = {}

    def __init__(self, app, port=None, host=None):
        self.app = app

        self.host = (
            host or
            capybara.server_host)

        self.port = (
            port or
            capybara.server_port or
            type(self)._ports.get(self.port_key, None) or
            find_available_port())

        self.server_thread = None

    @property
    def port_key(self):
        return str(id(self.app))

    @cached_property
    def middleware(self):
        return Middleware(self.app)

    def boot(self):
        """
        Boots a server for the app, if it isn't already booted.

        Returns:
            Server: This server.
        """

        if not self.responsive:
            # Remember the port so we can reuse it if we try to serve this same app again.
            type(self)._ports[self.port_key] = self.port

            init_func = capybara.servers[capybara.server_name]
            init_args = (self.middleware, self.port, self.host)

            self.server_thread = Thread(target=init_func, args=init_args)

            # Inform Python that it shouldn't wait for this thread to terminate before
            # exiting. (It will still be appropriately terminated when the process exits.)
            self.server_thread.daemon = True

            self.server_thread.start()

            # Make sure the server actually starts and becomes responsive.
            with timeout(60):
                while not self.responsive:
                    self.server_thread.join(0.1)

        return self

    @property
    def responsive(self):
        """ bool: Whether the server for this app is up and responsive. """

        if self.server_thread and self.server_thread.join(0):
            return False

        try:
            # Try to fetch the endpoint added by the middleware.
            with closing(urlopen("http://{0}:{1}/__identify__".format(self.host, self.port))) as response:
                body, status_code = response.read(), response.getcode()

                if str(status_code)[0] == "2" or str(status_code)[0] == "3":
                    return decode_body(body) == str(id(self.app))
        except URLError:
            pass

        return False


class Middleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        if environ["PATH_INFO"] == "/__identify__":
            return self.identify(environ, start_response)
        else:
            return self.app(environ, start_response)

    def identify(self, environ, start_response):
        start_response("200 OK", [("Content-Type", "text/plain")])
        return [encode_body(str(id(self.app)))]


if sys.version_info >= (3, 0):
    def decode_body(body):
        return body.decode()

    def encode_body(body):
        return body.encode()
else:
    def decode_body(body):
        return body

    def encode_body(body):
        return body
