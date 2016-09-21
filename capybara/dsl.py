from functools import wraps
import sys

import capybara
from capybara import DSL_METHODS as PACKAGE_METHODS
from capybara.session import DSL_METHODS as SESSION_METHODS, Session


__all__ = ["page"] + SESSION_METHODS + PACKAGE_METHODS


class Page(object):
    """ A proxy for the current session. """
    def __getattr__(self, attr):
        return getattr(capybara.current_session(), attr)


page = Page()
""" The singleton current-session proxy object. """


class DSLMixin:
    """ A mixin for including DSL methods in another class. """
    pass


_module_name = globals()["__name__"]
_module = sys.modules[_module_name]


def _define_package_method(name):
    func = getattr(capybara, name)

    setattr(DSLMixin, name, func)
    setattr(_module, name, func)


def _define_session_method(name):
    @wraps(getattr(Session, name))
    def func(*args, **kwargs):
        return getattr(page, name)(*args, **kwargs)

    setattr(DSLMixin, name, func)
    setattr(_module, name, func)


for _method in PACKAGE_METHODS:
    _define_package_method(_method)


for _method in SESSION_METHODS:
    _define_session_method(_method)
