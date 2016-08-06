from xpath.expression import ExpressionType
from xpath.renderer import to_xpath

from capybara.helpers import desc
from capybara.selector import selectors


class SelectorQuery(object):
    """
    Queries for elements using a selector.

    Args:
        selector (str): The name of the selector to use.
        locator (str): An identifying string to use to locate desired elements.
        exact (bool, optional): Whether to exactly match the locator string. Defaults to False.
    """

    def __init__(self, selector, locator, exact=None):
        self.selector = selectors[selector]
        self.expression = self.selector(locator)
        self.locator = locator
        self.options = {
            "exact": exact}

    @property
    def label(self):
        """ str: A short description of the selector. """
        return self.selector.label or self.selector.name

    @property
    def description(self):
        """ str: A long description of this query. """
        return "{} {}".format(self.label, desc(self.locator))

    @property
    def exact(self):
        """ bool: Whether to exactly match the locator string. """
        if self.options["exact"] is not None:
            return self.options["exact"]
        else:
            return False

    @property
    def xpath(self):
        """ str: The XPath query for this selector. """
        if isinstance(self.expression, ExpressionType):
            return to_xpath(self.expression, exact=self.exact)
        else:
            return str(self.expression)

    def resolve_for(self, node):
        """
        Resolves this query relative to the given node.

        Args:
            node (node.Base): The node relative to which this query should be resolved.

        Returns:
            list[Element]: A list of elements matched by this query.
        """

        from capybara.node.element import Element

        @node.synchronize
        def resolve():
            children = node._find_xpath(self.xpath)
            return [Element(node.session, child) for child in children]

        return resolve()
