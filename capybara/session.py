from contextlib import contextmanager
from functools import wraps
import sys
if sys.version_info >= (3, 0):
    from urllib.parse import ParseResult, urlparse
else:
    from urlparse import ParseResult, urlparse

import capybara
from capybara.node.base import Base
from capybara.node.document import Document
from capybara.node.element import Element
from capybara.server import Server
from capybara.utils import cached_property


_DOCUMENT_METHODS = ["assert_title", "has_title"]
_DOCUMENT_PROPERTIES = ["title"]
_NODE_METHODS = [
    "assert_selector", "assert_text", "check", "click_button", "click_link", "find", "find_button",
    "find_link", "has_button", "has_content", "has_css", "has_link", "has_selector", "has_text",
    "has_xpath", "uncheck"]
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

        session.click_button("Search")
        assert session.has_text("Capybara")

    Args:
        mode (str): The name of the driver to use.
        app (object): The WSGI-compliant app with which to interact.
    """

    def __init__(self, mode, app):
        self.mode = mode
        self.app = app
        self.server = Server(app).boot()
        self.synchronized = False
        self._scopes = [None]

    @cached_property
    def driver(self):
        """ driver.Base: The driver for the current session. """
        return capybara.drivers[self.mode](self.app)

    @cached_property
    def document(self):
        """ Document: The document for the current page. """
        return Document(self, self.driver)

    @property
    def current_scope(self):
        """ node.Base: The current node relative to which all interaction will be scoped. """
        return self._scopes[-1] or self.document

    @property
    def html(self):
        """ str: A snapshot of the DOM of the current document, as it looks right now. """
        return self.driver.html

    body = html
    """ Alias for :attr:`html`. """

    source = html
    """ Alias for :attr:`html`. """

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

    @contextmanager
    def scope(self, *args, **kwargs):
        """
        Executes the wrapped code within the context of a node. ``scope`` takes the same options
        as :meth:`find`. For the duration of the context, any command to Capybara will be handled
        as though it were scoped to the given element. ::

            with scope("xpath", "//div[@id='delivery-address']"):
                click_link("Edit")

        Just as with :meth:`find`, if multiple elements match the selector given to ``scope``, an
        error will be raised, and just as with :meth:`find`, this behavior can be controlled
        through the ``exact`` option.

        It is possible to omit the first argument, in that case, the selector is assumed to be of
        the type set in :data:`capybara.default_selector`. ::

            with scope("div#delivery-address"):
                click_link("Edit")

        Note that a lot of uses of ``scope`` can be replaced more succinctly with chaining::

            find("div#delivery-address").click_link("Edit")

        Args:
            *args: Variable length argument list for the call to :meth:`find`.
            **kwargs: Arbitrary keywords arguments for the call to :meth:`find`.
        """

        new_scope = args[0] if isinstance(args[0], Base) else self.find(*args, **kwargs)
        self._scopes.append(new_scope)
        try:
            yield
        finally:
            self._scopes.pop()

    @contextmanager
    def frame(self, locator):
        """
        Execute the wrapped code within the given iframe using the given frame or frame name/id.
        May not be supported by all drivers.

        Args:
            locator (str | Element): The name/id of the frame or the frame's element.
        """

        self._scopes.append(None)
        try:
            new_frame = locator if isinstance(locator, Element) else self.find("frame", locator)
            self.driver.switch_to_frame(new_frame)
            try:
                yield
            finally:
                self.driver.switch_to_frame("parent")
        finally:
            self._scopes.pop()

def _define_document_method(method_name):
    @wraps(getattr(Document, method_name))
    def func(self, *args, **kwargs):
        return getattr(self.document, method_name)(*args, **kwargs)
    setattr(Session, method_name, func)


def _define_document_property(property_name):
    def fget(self):
        return getattr(self.document, property_name)
    fdoc = getattr(Document, property_name).__doc__
    setattr(Session, property_name, property(fget, None, None, fdoc))


def _define_node_method(method_name):
    @wraps(getattr(Base, method_name))
    def func(self, *args, **kwargs):
        return getattr(self.current_scope, method_name)(*args, **kwargs)
    setattr(Session, method_name, func)


def _define_node_property(property_name):
    def fget(self):
        return getattr(self.current_scope, property_name)
    fdoc = getattr(Base, property_name).__doc__
    setattr(Session, property_name, property(fget, None, None, fdoc))


for method_name in _DOCUMENT_METHODS:
    _define_document_method(method_name)

for property_name in _DOCUMENT_PROPERTIES:
    _define_document_property(property_name)

for method_name in _NODE_METHODS:
    _define_node_method(method_name)

for property_name in _NODE_PROPERTIES:
    _define_node_property(property_name)
