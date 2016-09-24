from contextlib import contextmanager
from datetime import datetime
from functools import wraps
import os
import random
import sys
if sys.version_info >= (3, 0):
    from urllib.parse import ParseResult, urlparse
else:
    from urlparse import ParseResult, urlparse

import capybara
from capybara.exceptions import ScopeError, WindowError
from capybara.node.base import Base
from capybara.node.document import Document
from capybara.node.element import Element
from capybara.server import Server
from capybara.session_matchers import SessionMatchersMixin
from capybara.utils import cached_property, encode_string
from capybara.window import Window


_DOCUMENT_METHODS = ["assert_no_title", "assert_title", "has_no_title", "has_title"]
_DOCUMENT_PROPERTIES = ["title"]
_NODE_METHODS = [
    "assert_no_selector", "assert_no_text", "assert_selector", "assert_text", "attach_file",
    "check", "choose", "click_button", "click_link", "click_link_or_button", "click_on", "fill_in",
    "find", "find_all", "find_button", "find_by_id", "find_field", "find_first", "find_link",
    "has_button", "has_checked_field", "has_content", "has_css", "has_field", "has_link",
    "has_no_button", "has_no_checked_field", "has_no_css", "has_no_field", "has_no_link",
    "has_no_select", "has_no_selector", "has_no_table", "has_no_text", "has_no_unchecked_field",
    "has_no_xpath", "has_select", "has_selector", "has_table", "has_text", "has_unchecked_field",
    "has_xpath", "select", "uncheck", "unselect"]
_NODE_PROPERTIES = ["text"]
_SESSION_METHODS = [
    "accept_alert", "accept_confirm", "accept_prompt", "assert_current_path",
    "assert_no_current_path", "dismiss_confirm", "dismiss_prompt", "evaluate_script",
    "execute_script", "fieldset", "frame", "go_back", "go_forward", "has_current_path",
    "has_no_current_path", "open_new_window", "reset", "save_page", "save_screenshot", "scope",
    "switch_to_window", "table", "visit", "window", "window_opened_by"]
_SESSION_PROPERTIES = ["current_host", "current_path", "current_url", "current_window", "windows"]

DSL_METHODS = _DOCUMENT_METHODS + _NODE_METHODS + _SESSION_METHODS


class Session(SessionMatchersMixin, object):
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

    When using :mod:`capybara.dsl`, the Session is initialized automatically for you.

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

    def go_back(self):
        """ Move back a single entry in the browser's history. """
        self.driver.go_back()

    def go_forward(self):
        """ Move forward a single entry in the browser's history. """
        self.driver.go_forward()

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
        through the ``match`` and ``exact`` options.

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
    def fieldset(self, locator):
        """
        Execute the wrapped code within a specific fieldset given the id or legend of that
        fieldset.

        Args:
            locator (str): The id or legend of the fieldset.
        """

        with self.scope("fieldset", locator):
            yield

    @contextmanager
    def table(self, locator):
        """
        Execute the wrapped code within a specific table given the id or caption of that table.

        Args:
            locator (str): The id or caption of the table.
        """

        with self.scope("table", locator):
            yield

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

    @property
    def current_window(self):
        """ Window: The current window. """
        return Window(self, self.driver.current_window_handle)

    @property
    def windows(self):
        """
        Get all opened windows. The order of the windows in the returned list is not defined. The
        driver may sort windows by their creation time but it's not required.

        Returns:
            List[Window]: A list of all windows.
        """

        return [Window(self, window_handle) for window_handle in self.driver.window_handles]

    def open_new_window(self):
        """
        Open new window. The current window doesn't change as a result of this call. It should be
        switched explicitly.

        Returns:
            Window: The window that has been opened.
        """

        return self.window_opened_by(lambda: self.driver.open_new_window())

    def switch_to_window(self, window, wait=None):
        """
        If ``window`` is a lambda, it switches to the first window for which ``window`` returns a
        value other than False or None. If a window that matches can't be found, the window will be
        switched back and :exc:`WindowError` will be raised.

        Args:
            window (Window | lambda): The window that should be switched to, or a filtering lambda.
            wait (int | float, optional): The number of seconds to wait to find the window.

        Returns:
            Window: The new current window.

        Raises:
            ScopeError: If this method is invoked inside :meth:`scope, :meth:`frame`, or
                :meth:`window`.
            WindowError: If no window matches the given lambda.
        """

        if len(self._scopes) > 1:
            raise ScopeError(
                "`switch_to_window` is not supposed to be invoked from "
                "within `scope`s, `frame`s, or other `window`s.")

        if isinstance(window, Window):
            self.driver.switch_to_window(window.handle)
            return window
        else:
            @self.document.synchronize(errors=(WindowError,), wait=wait)
            def switch_and_get_matching_window():
                original_window_handle = self.driver.current_window_handle
                try:
                    for handle in self.driver.window_handles:
                        self.driver.switch_to_window(handle)
                        result = window()
                        if result:
                            return Window(self, handle)
                except Exception:
                    self.driver.switch_to_window(original_window_handle)
                    raise

                self.driver.switch_to_window(original_window_handle)
                raise WindowError("Could not find a window matching lambda")

            return switch_and_get_matching_window()

    @contextmanager
    def window(self, window):
        """
        This method does the following:

        1. Switches to the given window (it can be located by window instance/lambda/string).
        2. Executes the given block (within window located at previous step).
        3. Switches back (this step will be invoked even if exception happens at second step).

        Args:
            window (Window | lambda): The desired :class:`Window`, or a lambda that will be run in
                the context of each open window and returns ``True`` for the desired window.
        """

        original = self.current_window
        if window != original:
            self.switch_to_window(window)
        self._scopes.append(None)
        try:
            yield
        finally:
            self._scopes.pop()
            if original != window:
                self.switch_to_window(original)

    def window_opened_by(self, trigger_func, wait=None):
        """
        Get the window that has been opened by the passed lambda. It will wait for it to be opened
        (in the same way as other Capybara methods wait). It's better to use this method than
        ``windows[-1]`` `as order of windows isn't defined in some drivers`__.

        __ https://dvcs.w3.org/hg/webdriver/raw-file/default/webdriver-spec.html#h_note_10

        Args:
            trigger_func (func): The function that should trigger the opening of a new window.
            wait (int | float, optional): Maximum wait time. Defaults to
                :data:`capybara.default_max_wait_time`.

        Returns:
            Window: The window that has been opened within the lambda.

        Raises:
            WindowError: If lambda passed to window hasn't opened window or opened more than one
                window.
        """

        old_handles = set(self.driver.window_handles)
        trigger_func()

        @self.document.synchronize(wait=wait, errors=(WindowError,))
        def get_new_window():
            opened_handles = set(self.driver.window_handles) - old_handles
            if len(opened_handles) != 1:
                raise WindowError("lambda passed to `window_opened_by` "
                                  "opened {0} windows instead of 1".format(len(opened_handles)))
            return Window(self, list(opened_handles)[0])

        return get_new_window()

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

    def save_page(self, path=None):
        """
        Save a snapshot of the page.

        If invoked without arguments, it will save a file to :data:`capybara.save_path` and the
        file will be given a randomly generated filename. If invoked with a relative path, the path
        will be relative to :data:`capybara.save_path`.

        Args:
            path (str, optional): The path to where it should be saved.

        Returns:
            str: The path to which the file was saved.
        """

        path = _prepare_path(path, "html")

        with open(path, "wb") as f:
            f.write(encode_string(self.body))

        return path

    def save_screenshot(self, path=None, **kwargs):
        """
        Save a screenshot of the page.

        If invoked without arguments, it will save a file to :data:`capybara.save_path` and the
        file will be given a randomly generated filename. If invoked with a relative path, the path
        will be relative to :data:`capybara.save_path`.

        Args:
            path (str, optional): The path to where it should be saved.
            **kwargs: Arbitrary keywords arguments for the driver.

        Returns:
            str: The path to which the file was saved.
        """

        path = _prepare_path(path, "png")
        self.driver.save_screenshot(path, **kwargs)
        return path

    def reset(self):
        """
        Reset the session (i.e., remove cookies and navigate to a blank page).

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


def _prepare_path(path, extension):
    save_path = capybara.save_path or os.getcwd()
    path = os.path.normpath(os.path.join(save_path, path or _default_fn(extension)))

    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    return path


def _default_fn(extension):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return "capybara-{timestamp}{random}.{extension}".format(
        timestamp=timestamp,
        random=random.randint(0, 10**10),
        extension=extension)
