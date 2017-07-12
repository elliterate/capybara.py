from __future__ import absolute_import
from contextlib import contextmanager


app = None
""" object: The WSGI-compliant app to test. """

app_host = None
""" str: The default host to use when giving a relative URL to visit. Must be a valid URL. """

default_driver = "werkzeug"
""" str: The name of the driver default driver to use. """

javascript_driver = "selenium"
""" str: The name of the driver to use when JavaScript is required. """

current_driver = None
""" str: The name of the driver currently in use. """

server_name = "default"
""" str: The name of the server to use to serve the app. """

server_host = "127.0.0.1"
""" str: The IP address bound by the default server. """

server_port = None
""" int, optional: The port bound by the default server. """

automatic_label_click = False
""" bool: Whether checkbox/radio actions will try to click the label of invisible elements. """

automatic_reload = True
""" bool: Whether to automatically reload elements as Capybara is waiting. """

enable_aria_label = False
""" bool: Whether fields, links, and buttons will match against aria-label attributes. """

exact = False
""" bool: Whether to match the exact label name/contents. """

default_max_wait_time = 2
""" int: The maximum number of seconds to wait for asynchronous processes to finish. """

default_selector = "css"
""" str: The name of the default selector used to find elements. """

ignore_hidden_elements = True
""" bool: Whether to ignore hidden elements on the page. """

match = "smart"
""" str: The matching strategy to use. """

raise_server_errors = True
""" bool: Whether errors raised in the server should be raised in the tests. """

save_path = None
""" str, optional: Where to put saved pages and screenshots. """

visible_text_only = False
""" bool: Whether to only consider visible text. """

wait_on_first_by_default = False
""" bool: Whether :meth:`find_first` should wait for at least one element to appear. """

servers = {}
# Dict[str, Callable[[object, str, int], None]]: A dictionary of server initialization functions.

drivers = {}
# Dict[str, Callable[[object], object]]: A dictionary of driver initialization functions.

session_name = "default"
""" str: The current session name. """

_session_pool = {}
# Dict[str, Session]: A pool of `Session` objects, keyed by driver and app.


DSL_METHODS = ["using_session", "using_wait_time"]


def register_server(name):
    """
    Register a server initialization function.

    Args:
        name (str): The name of the server.

    Returns:
        Callable[[Callable[[object, str, int], None]], None]: A decorator that takes a function
            that initializes a server for the given WSGI-compliant app, host, and port.
    """

    def register(init_func):
        servers[name] = init_func

    return register


def register_driver(name):
    """
    Register a driver initialization function.

    Args:
        name (str): The name of the driver.

    Returns:
        Callable[[Callable[[object], object], None]: A decorator that takes a function that
            initializes a driver for the given WSGI-compliant app.
    """

    def register(init_func):
        drivers[name] = init_func

    return register


def run_default_server(app, port):
    servers["werkzeug"](app, port, server_host)


def use_default_driver():
    """ Use the default driver as the current driver. """
    global current_driver
    current_driver = None


@contextmanager
def using_driver(driver):
    """
    Execute the wrapped code using a specific driver.

    Args:
        driver (str): The name of the desired driver.
    """

    global current_driver

    original_current_driver = current_driver
    current_driver = driver
    try:
        yield
    finally:
        current_driver = original_current_driver


@contextmanager
def using_wait_time(seconds):
    """
    Execute a context using a specific wait time.

    Args:
        seconds (int | float): The new wait time.
    """

    global default_max_wait_time

    original_max_wait_time = default_max_wait_time
    default_max_wait_time = seconds
    try:
        yield
    finally:
        default_max_wait_time = original_max_wait_time


def current_session():
    """
    Returns the :class:`Session` for the current driver and app, instantiating one if needed.

    Returns:
        Session: The :class:`Session` for the current driver and app.
    """

    driver = current_driver or default_driver

    session_key = "{driver}:{session}:{app}".format(
        driver=driver, session=session_name, app=str(id(app)))
    session = _session_pool.get(session_key, None)

    if session is None:
        from capybara.session import Session
        session = Session(driver, app)
        _session_pool[session_key] = session

    return session


@contextmanager
def using_session(name):
    """
    Execute the wrapped code using a specific session name.

    Args:
        name (str): The name of the session to use.
    """

    global session_name

    previous_session_name = session_name
    session_name = name
    try:
        yield
    finally:
        session_name = previous_session_name


def reset_sessions():
    """ Resets all sessions. """

    for session in iter(_session_pool.values()):
        session.reset()


reset = reset_sessions
""" Alias for :func:`reset_sessions`. """


def string(html):
    """
    Wraps the given string, which should contain an HTML document or fragment in a :class:`Simple`
    which exposes :class:`MatchersMixin`, :class:`FindersMixin`, and :class:`DocumentMatchersMixin`.
    This allows you to query any string containing HTML in the exact same way you would query the
    current document in a Capybara session.

    Example: A single element ::

        node = Capybara.string(\"""<a href="foo">bar</a>\""")
        anchor = node.find_first("a")
        anchor["href"]  # => "foo"
        anchor.text  # => "bar"

    Example: Multiple elements ::

        node = Capybara.string(\"""
          <ul>
            <li id="home">Home</li>
            <li id="projects">Projects</li>
          </ul>
        \""")

        node.find("#projects").text  # => "Projects"
        node.has_selector("li#home", text="Home")
        node.has_selector("#projects")
        node.find("ul").find("li:first-child").text  # => "Home"

    Args:
        html (str | lxml.etree.Element): An HTML fragment or document.

    Returns:
        Simple: A node which has Capybara's finders and matchers.
    """

    from capybara.node.simple import Simple

    return Simple(html)


@register_server("default")
def init_default_server(app, port, host):
    run_default_server(app, port)


@register_server("werkzeug")
def init_werkzeug_server(app, port, host):
    try:
        import werkzeug
    except ImportError:
        raise ImportError(
            'Capybara\'s werkzeug server is unable to load `werkzeug`, please install the package '
            'and add `werkzeug` to your requirements.txt file.')

    from werkzeug.serving import make_server
    from logging import getLogger

    # Mute the server.
    log = getLogger('werkzeug')
    log.disabled = True

    server = make_server(host, port, app, threaded=True)

    # Inform Python that it shouldn't wait for request threads to terminate before
    # exiting. (They will still be appropriately terminated when the process exits.)
    server.daemon_threads = True

    server.serve_forever()


@register_driver("selenium")
def init_selenium_driver(app):
    try:
        import selenium
    except ImportError:
        raise ImportError(
            'Capybara\'s selenium driver is unable to load `selenium`, please install the package '
            'and add `selenium` to your requirements.txt file.')

    from capybara.selenium.driver import Driver

    return Driver(app)


@register_driver("werkzeug")
def init_werkzeug_driver(app):
    try:
        import werkzeug
    except ImportError:
        raise ImportError(
            'Capybara\'s werkzeug driver is unable to load `werkzeug`, please install the package '
            'and add `werkzeug` to your requirements.txt file.')

    from capybara.werkzeug.driver import Driver

    return Driver(app)
