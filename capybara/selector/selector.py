from contextlib import contextmanager

from capybara.selector.filter import Filter
from capybara.selector.filter_set import filter_sets
from capybara.utils import setter_decorator


selectors = {}
# Dict[str, Selector]: A dictionary of :class:`Selector` objects keyed by name. """


class Selector(object):
    """
    A callable object used for selecting elements in a document or node.

    Args:
        name (str): The name of the selector.
        label (str, optional): The label to use when describing this selector.
        descriptions (List[Callable[[Dict[str, Any]], str]]): Functions that build a description of
            the given filter options.
        css (Callable[[str], str], optional): A function to generate a CSS selector given a locator
            string.
        xpath (Callable[[str], str], optional): A function to generate an XPath query given a
            locator string.
        custom_filters (Dict[str, Filter]): A dictionary of filters this selector should use
            to identify matching elements. Defaults to {}.
    """

    def __init__(self, name, label=None, descriptions=None, css=None, xpath=None,
                 custom_filters=None):
        self.name = name
        self.label = label
        self.descriptions = descriptions or []
        self.css = css
        self.xpath = xpath
        self.format = "xpath" if xpath else "css"
        self.custom_filters = custom_filters or {}

    def __call__(self, locator):
        assert self.format, "selector has no format"
        return getattr(self, self.format)(locator)

    def description(self, options):
        """
        Returns a description of the given filter options relevant to this selector.

        Args:
            options (Dict[str, Any]): The filter options to describe.

        Returns:
            str: A description of the filter options.
        """

        return "".join([describe(options) for describe in self.descriptions])


class SelectorFactory(object):
    """
    A factory for configuring and building :class:`Selector` instances.

    Args:
        name (str): The name of the selector.
    """

    def __init__(self, name):
        self.name = name
        self.label = None
        self.descriptions = []
        self.func = None
        self.format = None
        self.custom_filters = {}

    def describe(self, func):
        """
        Decorates a function that builds a description of some selector options.

        Args:
            func (Callable[[Dict[str, Any]], str]): The description builder function.
        """

        self.descriptions.append(func)

    @setter_decorator
    def css(self, func):
        """
        Sets the given function as the CSS selector generation function.

        Args:
            func (Callable[[str], str]): The CSS selector generation function.
        """

        self.func = func
        self.format = "css"

    @setter_decorator
    def xpath(self, func):
        """
        Sets the given function as the XPath query generation function.

        Args:
            func (Callable[[str], str]): The XPath query generation function.
        """

        self.func = func
        self.format = "xpath"

    def filter(self, name, **kwargs):
        """
        Returns a decorator function for adding afilter.

        Args:
            name (str): The name of the filter.
            **kwargs: Variable keyword arguments for the filter.

        Returns:
            Callable[[Callable[[Element, Any], bool]]]: A decorator function for adding a filter.
        """

        def decorator(func):
            self.custom_filters[name] = Filter(name, func, **kwargs)

        return decorator

    def filter_set(self, name):
        """
        Adds filters from a particular global :class:`FilterSet`.

        Args:
            name (str): The name of the set whose filters should be added.
        """

        filter_set = filter_sets[name]
        for name, filter_ in iter(filter_set.filters.items()):
            self.custom_filters[name] = filter_
        self.descriptions += filter_set.descriptions

    def build_selector(self):
        """ Selector: Returns a new :class:`Selector` instance with the current configuration. """

        kwargs = {
            'label': self.label,
            'descriptions': self.descriptions,
            'custom_filters': self.custom_filters}
        if self.format == "xpath":
            kwargs['xpath'] = self.func
        if self.format == "css":
            kwargs['css'] = self.func

        return Selector(self.name, **kwargs)


@contextmanager
def add_selector(name):
    """
    Builds and registers a :class:`Selector` object with the given name and configuration.

    Args:
        name (str): The name of the selector.

    Yields:
        SelectorFactory: The factory that will build the :class:`Selector`.
    """

    factory = SelectorFactory(name)
    yield factory
    selectors[name] = factory.build_selector()


def remove_selector(name):
    """
    Unregisters selector with the given name.

    Args:
        name (str): The name of the selector.
    """

    selectors.pop(name, None)
