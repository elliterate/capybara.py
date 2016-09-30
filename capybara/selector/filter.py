from warnings import warn


class Filter(object):
    """
    A rule to apply to identify desired nodes.

    Args:
        name (str): The name of this filter.
        func (Callable[[Element, Any], bool]): A function that determines whether a given node
            matches a desired value.
        boolean (bool, optional): Whether the filter evaluates boolean values. Defaults to False.
        default (object, optional): A default desired value, if any. Defaults to None.
        skip_if (object, optional): A value which, if provided, signifies that this rule
            should be skipped.
        valid_values (List[Any], optional): The values the filter supports.
    """

    def __init__(self, name, func, boolean=None, default=None, skip_if=None, valid_values=None):
        self.name = name
        self.func = func
        self.default = default
        self.skip_if = skip_if
        self.valid_values = [True, False] if boolean else valid_values

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

        if not self._valid_value(value):
            msg = "Invalid value {value} passed to filter {name} - ".format(
                value=repr(value),
                name=self.name)

            if self.default is not None:
                warn(msg + "defaulting to {}".format(self.default))
                value = self.default
            else:
                warn(msg + "skipping")
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

    def _valid_value(self, value):
        """ bool: Whether the given value is valid. """

        if not self.valid_values:
            return True

        valid_values = (self.valid_values if isinstance(self.valid_values, list)
                        else list(self.valid_values))
        return value in valid_values
