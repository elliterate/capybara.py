from contextlib import closing
from threading import Thread

import capybara
from capybara.compat import URLError, decode_socket_data, encode_socket_data, urlopen
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
    def error(self):
        return self.middleware.error

    def reset_error(self):
        self.middleware.error = None

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
            identify_url = "http://{0}:{1}/__identify__".format(self.host, self.port)

            with closing(urlopen(identify_url)) as response:
                body, status_code = response.read(), response.getcode()

                if str(status_code)[0] == "2" or str(status_code)[0] == "3":
                    return decode_socket_data(body) == str(id(self.app))
        except URLError:
            pass

        return False


class Middleware(object):
    def __init__(self, app):
        self.app = app
        self.error = None

    def __call__(self, environ, start_response):
        if environ["PATH_INFO"] == "/__identify__":
            return self.identify(environ, start_response)
        else:
            try:
                return self.app(environ, start_response)
            except Exception as e:
                self.error = e
                raise

    def identify(self, environ, start_response):
        start_response("200 OK", [("Content-Type", "text/plain")])
        return [encode_socket_data(str(id(self.app)))]
