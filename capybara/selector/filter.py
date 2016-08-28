class Filter(object):
    """
    A rule to apply to identify desired nodes.

    Args:
        name (str): The name of this filter.
        func (Callable[[Element, Any], bool]): A function that determines whether a given node
            matches a desired value.
        default (object, optional): A default desired value, if any. Defaults to None.
        skip_if (object, optional): A value which, if provided, signifies that this rule
            should be skipped.
    """

    def __init__(self, name, func, default=None, skip_if=None):
        self.name = name
        self.func = func
        self.default = default
        self.skip_if = skip_if

    @property
    def has_default(self):
        """ bool: Whether this rule has a default desired value. """
        return self.default is not None

    @property
    def has_skip_if(self):
        """ bool: Whether this rule has a value for which it should be skipped. """
        return self.skip_if is not None

    def matches(self, node, value):
        """
        Returns whether the given node matches the filter rule with the given value.

        Args:
            node (Element): The node to filter.
            value (object): The desired value with which the node should be evaluated.

        Returns:
            bool: Whether the given node matches.
        """

        if self.skip(value):
            return True

        return self.func(node, value)

    def skip(self, value):
        """
        Returns whether this rule should be skipped for the given value.

        Args:
            value (Any): A value which may be used to match nodes.

        Returns:
            bool: Whether this rule should be skipped.
        """

        return self.has_skip_if and value == self.skip_if
