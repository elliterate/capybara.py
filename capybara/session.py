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
    "assert_selector", "assert_text", "check", "choose", "click_button", "click_link",
    "click_link_or_button", "click_on", "fill_in", "find", "find_button", "find_by_id", "find_field",
    "find_link", "has_button", "has_content", "has_css", "has_link", "has_selector", "has_text",
    "has_xpath", "select", "uncheck", "unselect"]
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
    such as :meth:`visit`, :attr:`current_path`, and so on. It also delegates a number of methods to
    a :class:`Document`, representing the current HTML document. This allows interaction::

        session.fill_in("q", value="Capybara")
        session.click_button("Search")
        assert session.has_text("Capybara")

    Args:
        mode (str): The name of the driver to use.
        app (object): The WSGI-compliant app with which to interact.
    """

    def __init__(self, mode, app):
        self.mode = mode
        self.app = app
        self.server = Server(app).boot() if app else None
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

    @property
    def current_path(self):
        """ str: Path of the current page, without any domain information. """
        path = urlparse(self.current_url).path
        return path if path else None

    @property
    def current_host(self):
        """ str: Host of the current page. """
        result = urlparse(self.current_url)
        scheme, netloc = result.scheme, result.netloc
        host = netloc.split(":")[0] if netloc else None
        return "{0}://{1}".format(scheme, host) if host else None

    @property
    def current_url(self):
        """ str: Fully qualified URL of the current page. """
        return self.driver.current_url

    def visit(self, visit_uri):
        """
        Navigate to the given URL. The URL can either be a relative URL or an absolute URL. The
        behavior of either depends on the driver. ::

            session.visit("/foo")
            session.visit("http://google.com")

        For drivers which can run against an external application, such as the Selenium driver,
        giving an absolute URL will navigate to that page. This allows testing applications running
        on remote servers. For these drivers, setting :data:`capybara.app_host` will make the
        remote server the default. For example::

            capybara.app_host = "http://google.com"
            session.visit("/")  # visits the Google homepage

        Args:
            visit_uri (str): The URL to navigate to.
        """

        visit_uri = urlparse(visit_uri)

        if capybara.app_host:
            uri_base = urlparse(capybara.app_host)
        elif self.server:
            uri_base = urlparse("http://{}:{}".format(self.server.host, self.server.port))
        else:
            uri_base = None

        visit_uri = ParseResult(
            scheme=visit_uri.scheme or (uri_base.scheme if uri_base else None),
            netloc=visit_uri.netloc or (uri_base.netloc if uri_base else None),
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
                fill_in("Street", value="12 Main Street")

        Just as with :meth:`find`, if multiple elements match the selector given to ``scope``, an
        error will be raised, and just as with :meth:`find`, this behavior can be controlled
        through the ``exact`` option.

        It is possible to omit the first argument, in that case, the selector is assumed to be of
        the type set in :data:`capybara.default_selector`. ::

            with scope("div#delivery-address"):
                fill_in("Street", value="12 Main Street")

        Note that a lot of uses of ``scope`` can be replaced more succinctly with chaining::

            find("div#delivery-address").fill_in("Street", value="12 Main Street")

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

    def execute_script(self, script):
        """
        Execute the given script, not returning a result. This is useful for scripts that return
        complex objects, such as jQuery statements. ``execute_script`` should be used over
        :meth:`evaluate_script` whenever possible.

        Args:
            script (str): A string of JavaScript to execute.
        """

        self.driver.execute_script(script)

    def evaluate_script(self, script):
        """
        Evaluate the given JavaScript and return the result. Be careful when using this with
        scripts that return complex objects, such as jQuery statements. :meth:`execute_script`
        might be a better alternative.

        Args:
            script (str): A string of JavaScript to evaluate.

        Returns:
            object: The result of the evaluated JavaScript (may be driver specific).
        """

        return self.driver.evaluate_script(script)

    @contextmanager
    def accept_alert(self, text=None, wait=None):
        """
        Execute the wrapped code, accepting an alert.

        Args:
            text (str, optional): Text to match against the text in the modal.
            wait (int | float, optional): Maximum time to wait for the modal to appear after
                executing the wrapped code.

        Raises:
            ModalNotFound: If a modal dialog hasn't been found.
        """

        wait = wait or capybara.default_max_wait_time
        with self.driver.accept_modal("alert", text=text, wait=wait):
            yield

    @contextmanager
    def accept_confirm(self, text=None, wait=None):
        """
        Execute the wrapped code, accepting a confirm.

        Args:
            text (str, optional): Text to match against the text in the modal.
            wait (int | float, optional): Maximum time to wait for the modal to appear after
                executing the wrapped code.

        Raises:
            ModalNotFound: If a modal dialog hasn't been found.
        """

        with self.driver.accept_modal("confirm", text=text, wait=wait):
            yield

    @contextmanager
    def dismiss_confirm(self, text=None, wait=None):
        """
        Execute the wrapped code, dismissing a confirm.

        Args:
            text (str, optional): Text to match against the text in the modal.
            wait (int | float, optional): Maximum time to wait for the modal to appear after
                executing the wrapped code.

        Raises:
            ModalNotFound: If a modal dialog hasn't been found.
        """

        with self.driver.dismiss_modal("confirm", text=text, wait=wait):
            yield

    @contextmanager
    def accept_prompt(self, text=None, response=None, wait=None):
        """
        Execute the wrapped code, accepting a prompt, optionally responding to the prompt.

        Args:
            text (str, optional): Text to match against the text in the modal.
            response (str, optional): Response to provide to the prompt.
            wait (int | float, optional): Maximum time to wait for the modal to appear after
                executing the wrapped code.

        Raises:
            ModalNotFound: If a modal dialog hasn't been found.
        """

        with self.driver.accept_modal("prompt", text=text, response=response, wait=wait):
            yield

    @contextmanager
    def dismiss_prompt(self, text=None, wait=None):
        """
        Execute the wrapped code, dismissing a prompt.

        Args:
            text (str, optional): Text to match against the text in the modal.
            wait (int | float, optional): Maximum time to wait for the modal to appear after
                executing the wrapped code.

        Raises:
            ModalNotFound: If a modal dialog hasn't been found.
        """

        with self.driver.dismiss_modal("prompt", text=text, wait=wait):
            yield

    def reset(self):
        """
        Reset the session (i.e., navigate to a blank page).

        This method does not:
        * accept modal dialogs if they are present (the Selenium driver does, but others may not),
        * clear the browser cache/HTML 5 local storage/IndexedDB/Web SQL database/etc., or
        * modify the state of the driver/underlying browser in any other way

        as doing so would result in performance downsides and it's not needed to do everything
        from the list above for most apps.

        If you want to do anything from the list above on a general basis you can write a test
        teardown method.
        """

        self.driver.reset()

    cleanup = reset
    """ Alias for :meth:`reset`. """

    reset_session = reset
    """ Alias for :meth:`reset`. """


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
