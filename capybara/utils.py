from contextlib import contextmanager
import signal
from socket import socket
from threading import Lock
from time import time

from capybara.compat import (
    ParseResult,
    bytes_,
    parse_qsl,
    quote,
    str_,
    unquote,
    urlencode,
    urlparse)


_missing = object()


class cached_property(property):
    """ Decorates an instance method, turning it into a property whose value is cached. """

    def __init__(self, func):
        self.__name__ = func.__name__
        self.__module__ = func.__module__
        self.__doc__ = func.__doc__
        self.func = func

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        value = obj.__dict__.get(self.__name__, _missing)
        if value is _missing:
            value = self.func(obj)
            obj.__dict__[self.__name__] = value
        return value


class Counter(object):
    """ Keeps track of a running count. """

    def __init__(self):
        self._lock = Lock()
        self._value = 0

    @property
    def value(self):
        """ int: The current value of the counter. """
        return self._value

    def __enter__(self):
        with self._lock:
            self._value += 1

    def __exit__(self, *args):
        with self._lock:
            self._value -= 1


def decode_bytes(value):
    """ str: Decodes the given byte sequence. """
    return value.decode("utf-8") if isbytes(value) else value


def encode_string(value):
    """ bytes: Encodes the given string. """
    return value.encode("utf-8") if isstring(value) else value


def find_available_port():
    """ int: A random available port. """
    s = socket()
    s.bind(("", 0))
    return s.getsockname()[1]


def inner_content(node):
    """
    Returns the inner content of a given XML node, including tags.

    Args:
        node (lxml.etree.Element): The node whose inner content is desired.

    Returns:
        str: The inner content of the node.
    """

    from lxml import etree

    # Include text content at the start of the node.
    parts = [node.text]

    for child in node.getchildren():
        # Include the child serialized to raw XML.
        parts.append(etree.tostring(child, encoding="utf-8"))

        # Include any text following the child.
        parts.append(child.tail)

    # Discard any non-existent text parts and return.
    return "".join(filter(None, parts))


def inner_text(node):
    """
    Returns the inner text of a given XML node, excluding tags.

    Args:
        node: (lxml.etree.Element): The node whose inner text is desired.

    Returns:
        str: The inner text of the node.
    """

    from lxml import etree

    # Include text content at the start of the node.
    parts = [node.text]

    for child in node.getchildren():
        # Include the raw text content of the child.
        parts.append(etree.tostring(child, encoding="utf-8", method="text"))

        # Include any text following the child.
        parts.append(child.tail)

    # Discard any non-existent text parts and return.
    return "".join(map(decode_bytes, filter(None, parts)))


def isbytes(value):
    """ bool: Whether the given value is a sequence of bytes. """
    return isinstance(value, bytes_)


def isregex(possible_regex):
    """
    Returns whether the given object is (probably) a regular expression object.

    Args:
        possible_regex (object): An object which may or may not be a regular expression.

    Returns:
        bool: Whether the given object is (probably) a regular expression object.
    """

    return hasattr(possible_regex, "search") and callable(possible_regex.search)


def isstring(value):
    """ bool: Whether the given value is a string. """
    return isinstance(value, str_)


def normalize_url(url):
    """
    Returns the given URL with all query keys properly escaped.

    Args:
        url (str): The URL to normalize.

    Returns:
        str: The normalized URL.
    """

    uri = urlparse(url)
    query = uri.query or ""

    pairs = parse_qsl(query)
    decoded_pairs = [(unquote(key), value) for key, value in pairs]
    encoded_pairs = [(quote(key), value) for key, value in decoded_pairs]
    normalized_query = urlencode(encoded_pairs)

    return ParseResult(
        scheme=uri.scheme,
        netloc=uri.netloc,
        path=uri.path,
        params=uri.params,
        query=normalized_query,
        fragment=uri.fragment).geturl()


def setter_decorator(fset):
    """
    Define a write-only property that, in addition to the given setter function, also
    provides a setter decorator defined as the property's getter function.

    This allows one to set the property either through traditional assignment, as a
    method argument, or through decoration::

        class Widget(object):
            @setter_decorator
            def handler(self, value):
                self._handler = value

        widget = Widget()

        # Method 1: Traditional assignment
        widget.handler = lambda input: process(input)

        # Method 2: Assignment via method argument
        widget.handler(lambda input: process(input))

        # Method 3: Assignment via decoration
        @widget.handler
        def handler(input):
            return process(input)

        # Method 3b: Assignment via decoration with extraneous parens
        @widget.handler()
        def handler(input):
            return process(input)
    """

    def fget(self):
        def inner(value):
            fset(self, value)

        def outer(value=None):
            if value:
                # We are being called with the desired value, either directly or
                # as a decorator.
                inner(value)
            else:
                # Assume we are being called as a decorator with extraneous parens,
                # so return the setter as the actual decorator.
                return inner

        return outer

    fdoc = fset.__doc__

    return property(fget, fset, None, fdoc)


class TimeoutError(Exception):
    pass


@contextmanager
def timeout(seconds):
    """
    Raises an exception if the wrapped code fails to return within the given number of seconds.

    Args:
        seconds (int | float): The number of seconds to wait before timing out.

    Raises:
        TimeoutError: The wrapped code failed to return within the given timeout.
    """

    def handler(signum, frame):
        raise TimeoutError()

    old_seconds, start_time = 0, 0
    old_handler = signal.signal(signal.SIGALRM, handler)
    try:
        start_time = time()
        old_seconds = signal.alarm(seconds)

        if 0 < old_seconds < seconds:
            # Someone else cares about a shorter timeout, so restore it.
            handler = None

            # Give ourselves a moment to restore before re-activating the alarm.
            signal.alarm(0)

            # Restore the original handler.
            signal.signal(signal.SIGALRM, old_handler)
            old_handler = None

            # Restore the original alarm.
            signal.alarm(old_seconds)
            old_seconds = 0

        try:
            yield
        finally:
            if handler:
                signal.alarm(0)
    finally:
        # If another handler was registered, restore it.
        if old_handler:
            signal.signal(signal.SIGALRM, old_handler)

        # If another alarm was already scheduled, restore it.
        if old_seconds:
            elapsed = time() - start_time
            signal.alarm(old_seconds - elapsed)
