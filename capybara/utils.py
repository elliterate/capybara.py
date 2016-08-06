from contextlib import contextmanager
import signal
from socket import socket
import sys
from time import time


_missing = object()

if sys.version_info >= (3, 0):
    _bytes = bytes
    _bytes_decode_attr_name = "decode"
else:
    _bytes = unicode
    _bytes_decode_attr_name = "encode"


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


def decode_bytes(value):
    """ str: Decodes the given byte sequence. """
    return getattr(value, _bytes_decode_attr_name)("utf-8")


def find_available_port():
    """ int: A random available port. """
    s = socket()
    s.bind(("", 0))
    return s.getsockname()[1]


def isbytes(value):
    """ bool: Whether the given value is a sequence of bytes. """
    return isinstance(value, _bytes)


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
