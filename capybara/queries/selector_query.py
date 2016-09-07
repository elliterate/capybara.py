from xpath.expression import ExpressionType
from xpath.renderer import to_xpath

import capybara
from capybara.helpers import desc
from capybara.result import Result
from capybara.selector import selectors


class SelectorQuery(object):
    """
    Queries for elements using a selector.

    If no locator is provided and the given selector is not a valid selector, the first
    argument is assumed to be the locator and the default selector will be used.

    Args:
        selector (str): The name of the selector to use.
        locator (str): An identifying string to use to locate desired elements.
        count (int, optional): The number of times the selector should match. Defaults to any number
            of times greater than zero.
        exact (bool, optional): Whether to exactly match the locator string. Defaults to False.
        visible (bool | str, optional): The desired element visibility. Defaults to
            :data:`capybara.ignore_hidden_elements`.
        **filter_options: Arbitrary keyword arguments for the selector's filters.
    """

    def __init__(self, selector, locator=None, count=None, exact=None, visible=None, **filter_options):
        if locator is None and selector not in selectors:
            locator = selector
            selector = capybara.default_selector

        self.selector = selectors[selector]
        self.expression = self.selector(locator)
        self.locator = locator
        self.options = {
            "count": count,
            "exact": exact,
            "visible": visible}
        self.filter_options = filter_options

    @property
    def name(self):
        """ str: The name of selector. """
        return self.selector.name

    @property
    def label(self):
        """ str: A short description of the selector. """
        return self.selector.label or self.selector.name

    @property
    def kwargs(self):
        """ Dict[str, Any]: The keyword arguments with which this query was initialized. """
        kwargs = {}
        kwargs.update(self.options)
        kwargs.update(self.filter_options)
        return kwargs

    @property
    def description(self):
        """ str: A long description of this query. """
        description = "{} {}".format(self.label, desc(self.locator))
        description += self.selector.description(self.filter_options)
        return description

    @property
    def exact(self):
        """ bool: Whether to exactly match the locator string. """
        if self.options["exact"] is not None:
            return self.options["exact"]
        else:
            return False

    @property
    def visible(self):
        """ str: The desired element visibility. """
        if self.options["visible"] is not None:
            if self.options["visible"] is True:
                return "visible"
            elif self.options["visible"] is False:
                return "all"
            else:
                return self.options["visible"]
        else:
            if capybara.ignore_hidden_elements:
                return "visible"
            else:
                return "all"

    @property
    def css(self):
        """ str: The CSS query for this selector. """
        return self.expression

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

        from capybara.driver.node import Node
        from capybara.node.element import Element
        from capybara.node.simple import Simple

        @node.synchronize
        def resolve():
            if self.selector.format == "css":
                children = node._find_css(self.css)
            else:
                children = node._find_xpath(self.xpath)

            def wrap(child):
                if isinstance(child, Node):
                    return Element(node.session, child, node, self)
                else:
                    return Simple(child)

            children = [wrap(child) for child in children]

            return Result(children, self)

        return resolve()

    def matches_filters(self, node):
        """
        Returns whether the given node matches all filters.

        Args:
            node (Element): The node to evaluate.

        Returns:
            bool: Whether the given node matches.
        """

        visible = self.visible
        if visible == "visible":
            if not node.visible:
                return False
        elif visible == "hidden":
            if node.visible:
                return False

        for name, query_filter in iter(self._query_filters.items()):
            if name in self.filter_options:
                if not query_filter.matches(node, self.filter_options[name]):
                    return False
            elif query_filter.has_default:
                if not query_filter.matches(node, query_filter.default):
                    return False
        return True

    @property
    def _query_filters(self):
        return self.selector.custom_filters
