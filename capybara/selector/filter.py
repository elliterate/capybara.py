class Filter(object):
    """
    A rule to apply to identify desired nodes.

    Args:
        name (str): The name of this filter.
        func (Callable[[Element, Any], bool]): A function that determines whether a given node
            matches a desired value.
        default (object, optional): A default desired value, if any. Defaults to None.
    """

    def __init__(self, name, func, default=None):
        self.name = name
        self.func = func
        self.default = default

    @property
    def has_default(self):
        """ bool: Whether this rule has a default desired value. """
        return self.default is not None

    def matches(self, node, value):
        """
        Returns whether the given node matches the filter rule with the given value.

        Args:
            node (Element): The node to filter.
            value (object): The desired value with which the node should be evaluated.

        Returns:
            bool: Whether the given node matches.
        """

        return self.func(node, value)
