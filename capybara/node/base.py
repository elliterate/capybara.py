from capybara.node.finders import FindersMixin
from capybara.node.matchers import MatchersMixin


class Base(FindersMixin, MatchersMixin, object):
    """
    A :class:`Base` represents either an element on a page through the subclass :class:`Element` or
    a document through :class:`Document`.

    Both types of Node share the same methods, used for interacting with the elements on the page.
    These methods are divided into two categories: finders and matchers. These are found in the
    classes :class:`FindersMixin` and :class:`MatchersMixin` respectively.

    A :class:`Session` exposes all methods from :class:`Document` directly::

        session = Session("selenium", my_app)
        session.visit("/")
        bar = session.find("#bar")  # from capybara.node.finders.FindersMixin

    Args:
        base (driver.Node): The underlying driver node.
    """

    def __init__(self, base):
        self.base = base

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

    def _find_xpath(self, xpath):
        return self.base._find_xpath(xpath)
