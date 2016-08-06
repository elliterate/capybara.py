from capybara.helpers import desc
from capybara.selector import selectors


class SelectorQuery(object):
    """
    Queries for elements using a selector.

    Args:
        selector (str): The name of the selector to use.
        locator (str): An identifying string to use to locate desired elements.
    """

    def __init__(self, selector, locator):
        self.selector = selectors[selector]
        self.expression = self.selector(locator)
        self.locator = locator

    @property
    def label(self):
        """ str: A short description of the selector. """
        return self.selector.name

    @property
    def description(self):
        """ str: A long description of this query. """
        return "{} {}".format(self.label, desc(self.locator))

    @property
    def xpath(self):
        """ str: The XPath query for this selector. """
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

        children = node._find_xpath(self.xpath)
        return [Element(child) for child in children]
