from contextlib import contextmanager

from capybara.selector.filter import Filter


filter_sets = {}
# Dict[str, FilterSet]: A dictionary of global filter sets keyed by name.


class FilterSet(object):
    """
    A group of filters for use by :class:`Selector` objects.

    Args:
        name (str): The name of this set of filters.
        descriptions (List[Callable[[Dict[str, Any]], str]]): Functions that generate descriptions
            for options.
        filters (Dict[str, Filter], optional): The filters in this set. Defaults to {}.
    """

    def __init__(self, name, descriptions=None, filters=None):
        self.name = name
        self.descriptions = descriptions or []
        self.filters = filters or {}

    def description(self, options):
        """
        Returns a description of the given filter options relevant to this filter set.

        Args:
            options (Dict[str, Any]): The filter options to describe.

        Returns:
            str: A description of the filter options.
        """

        return "".join([describe(options) for describe in self.descriptions])


class FilterSetFactory(object):
    """ A factory for configuring and building :class:`FilterSet` instances. """

    def __init__(self, name):
        self.name = name
        self.descriptions = []
        self.filters = {}

    def describe(self, func):
        """
        Decorates a function that builds a description of some filter set options.

        Args:
            func (Callable[[Dict[str, Any]], str]): The description builder function.
        """

        self.descriptions.append(func)

    def filter(self, name, **kwargs):
        """
        Returns a decorator function for adding filters to built sets.

        Args:
            name (str): The name of the filter.
            **kwargs: Variable keyword arguments for the filter.

        Returns:
            Callable[[Callable[[Element, Any], bool]]]: A decorator function for adding filters to
                built sets.
        """

        def decorator(func):
            self.filters[name] = Filter(name, func, **kwargs)

        return decorator

    def build_filter_set(self):
        """ FilterSet: Returns a new :class:`FilterSet` with the current factory config. """
        return FilterSet(self.name, self.descriptions, self.filters)


@contextmanager
def add_filter_set(name):
    """
    Builds and registers a global :class:`FilterSet`.

    Args:
        name (str): The name of the set.

    Yields:
        FilterSetFactory: A configurable factory for building a :class:`FilterSet`.
    """

    factory = FilterSetFactory(name)
    yield factory
    filter_sets[name] = factory.build_filter_set()


def remove_filter_set(name):
    """
    Unregisters filter set with the given name.

    Args:
        name (str): The name of the filter set.
    """

    filter_sets.pop(name, None)
