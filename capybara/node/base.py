from functools import wraps
from time import sleep, time

import capybara
from capybara.exceptions import ElementNotFound, FrozenInTime
from capybara.node.actions import ActionsMixin
from capybara.node.finders import FindersMixin
from capybara.node.matchers import MatchersMixin


class Base(FindersMixin, ActionsMixin, MatchersMixin, object):
    """
    A :class:`Base` represents either an element on a page through the subclass :class:`Element` or
    a document through :class:`Document`.

    Both types of Node share the same methods, used for interacting with the elements on the page.
    These methods are divided into three categories: finders, actions, and matchers. These are found
    in the classes :class:`FindersMixin`, :class:`ActionsMixin`, and :class:`MatchersMixin`
    respectively.

    A :class:`Session` exposes all methods from :class:`Document` directly::

        session = Session("selenium", my_app)
        session.visit("/")
        session.fill_in("Foo", value="Bar")  # from capybara.node.actions.ActionsMixin
        bar = session.find("#bar")           # from capybara.node.finders.FindersMixin
        bar.select("Baz", field="Quox")      # from capybara.node.actions.ActionsMixin
        session.has_css("#foobar")           # from capybara.node.matchers.MatchersMixin

    Args:
        session (Session): The session from which this node originated.
        base (driver.Node): The underlying driver node.
    """

    def __init__(self, session, base):
        self.session = session
        self.base = base
        self.allow_reload = False

    def reload(self):
        """
        Reloads the underlying driver node.

        Returns:
            node.Base: This node.
        """

        return self

    def __eq__(self, other):
        return id(self) == id(other) or (hasattr(other, "base") and self.base == other.base)

    def __hash__(self):
        return hash(self.base)

    def __getitem__(self, name):
        """
        Retrieve the given attribute.

        Args:
            name (str): The attribute to retrieve.

        Returns:
            str: The value of the attribute.
        """

        raise NotImplementedError()

    @property
    def text(self):
        """ str: The text of the node. """
        raise NotImplementedError()

    @property
    def all_text(self):
        """ str: All of the text of the node. """
        raise NotImplementedError()

    @property
    def visible_text(self):
        """ str: Only the visible text of the node. """
        raise NotImplementedError()

    def synchronize(self, func=None, wait=None, errors=()):
        """
        This method is Capybara's primary defense against asynchronicity problems. It works by
        attempting to run a given decorated function until it succeeds. The exact behavior of this
        method depends on a number of factors. Basically there are certain exceptions which, when
        raised from the decorated function, instead of bubbling up, are caught, and the function is
        re-run.

        Certain drivers have no support for asynchronous processes. These drivers run the function,
        and any error raised bubbles up immediately. This allows faster turn around in the case
        where an expectation fails.

        Only exceptions that are :exc:`ElementNotFound` or any subclass thereof cause the block to
        be rerun. Drivers may specify additional exceptions which also cause reruns. This usually
        occurs when a node is manipulated which no longer exists on the page. For example, the
        Selenium driver specifies ``selenium.common.exceptions.StateElementReferenceException``.

        As long as any of these exceptions are thrown, the function is re-run, until a certain
        amount of time passes. The amount of time defaults to :data:`capybara.default_max_wait_time`
        and can be overridden through the ``wait`` argument. This time is compared with the system
        time to see how much time has passed. If the return value of ``time.time()`` is stubbed
        out, Capybara will raise :exc:`FrozenInTime`.

        Args:
            func (Callable, optional): The function to decorate.
            wait (int, optional): Number of seconds to retry this function.
            errors (Tuple[Type[Exception]], optional): Exception types that cause the function to be
                rerun. Defaults to ``driver.invalid_element_errors`` + :exc:`ElementNotFound`.

        Returns:
            Callable: The decorated function, or a decorator function.

        Raises:
            FrozenInTime: If the return value of ``time.time()`` appears stuck.
        """

        def decorator(func):
            @wraps(func)
            def outer(*args, **kwargs):
                caught_errors = (
                    errors or
                    self.session.driver.invalid_element_errors + (ElementNotFound,))
                seconds = wait if wait is not None else capybara.default_max_wait_time

                def inner():
                    return func(*args, **kwargs)

                if self.session.synchronized:
                    return inner()
                else:
                    start_time = time()
                    self.session.synchronized = True
                    try:
                        while True:
                            try:
                                return inner()
                            except Exception as e:
                                if not isinstance(e, caught_errors):
                                    raise
                                if time() - start_time >= seconds:
                                    raise

                                sleep(0.05)

                                if time() == start_time:
                                    raise FrozenInTime(
                                        "time appears to be frozen, Capybara does not work with "
                                        "libraries which freeze time, consider using time "
                                        "traveling instead")
                                if capybara.automatic_reload:
                                    self.reload()
                    finally:
                        self.session.synchronized = False

            return outer

        if func:
            return decorator(func)
        else:
            return decorator

    def _find_css(self, css):
        return self.base._find_css(css)

    def _find_xpath(self, xpath):
        return self.base._find_xpath(xpath)


def synchronize(func):
    """ Decorator for :meth:`synchronize`. """

    @wraps(func)
    def outer(self, *args, **kwargs):
        @self.synchronize
        def inner(self, *args, **kwargs):
            return func(self, *args, **kwargs)

        return inner(self, *args, **kwargs)

    return outer
