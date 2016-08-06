from functools import wraps
import sys
if sys.version_info >= (3, 0):
    from urllib.parse import ParseResult, urlparse
else:
    from urlparse import ParseResult, urlparse

import capybara
from capybara.node.document import Document
from capybara.server import Server
from capybara.utils import cached_property


_NODE_METHODS = ["assert_text", "find", "find_link", "has_content", "has_text"]
_NODE_PROPERTIES = ["text"]


class Session(object):
    """
    The Session class represents a single user's interaction with the system. The Session can use
    any of the underlying drivers. A session can be initialized manually like this::

        session = Session("selenium", MyWSGIApp)

    The application given as the second argument is optional. When running Capybara against an
    external page, you might want to leave it out::

        session = Session("selenium")
        session.visit("http://www.google.com")

    Session provides a number of methods and properties for controlling the navigation of the page,
    such as :meth:`visit` and so on. It also delegates a number of methods to a :class:`Document`,
    representing the current HTML document. This allows interaction::

        assert session.has_text("Capybara")

    Args:
        mode (str): The name of the driver to use.
        app (object): The WSGI-compliant app with which to interact.
    """

    def __init__(self, mode, app):
        self.mode = mode
        self.app = app
        self.server = Server(app).boot()

    @cached_property
    def driver(self):
        """ driver.Base: The driver for the current session. """
        return capybara.drivers[self.mode](self.app)

    @cached_property
    def document(self):
        """ Document: The document for the current page. """
        return Document(self.driver)

    def visit(self, visit_uri):
        """
        Navigate to the given URL. ::

            session.visit("/foo")

        Args:
            visit_uri (str): The URL to navigate to.
        """

        visit_uri = urlparse(visit_uri)
        uri_base = urlparse("http://{0}:{1}".format(self.server.host, self.server.port))

        visit_uri = ParseResult(
            scheme=uri_base.scheme,
            netloc=uri_base.netloc,
            path=visit_uri.path,
            params=visit_uri.params,
            query=visit_uri.query,
            fragment=visit_uri.fragment)

        self.driver.visit(visit_uri.geturl())


def _define_node_method(method_name):
    @wraps(getattr(Document, method_name))
    def func(self, *args, **kwargs):
        return getattr(self.document, method_name)(*args, **kwargs)
    setattr(Session, method_name, func)


def _define_node_property(property_name):
    def fget(self):
        return getattr(self.document, property_name)
    fdoc = getattr(Document, property_name).__doc__
    setattr(Session, property_name, property(fget, None, None, fdoc))


for method_name in _NODE_METHODS:
    _define_node_method(method_name)

for property_name in _NODE_PROPERTIES:
    _define_node_property(property_name)
