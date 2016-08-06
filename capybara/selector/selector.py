from contextlib import contextmanager

from capybara.utils import setter_decorator


selectors = {}
# Dict[str, Selector]: A dictionary of :class:`Selector` objects keyed by name. """


class Selector(object):
    """
    A callable object used for selecting elements in a document or node.

    Args:
        name (str): The name of the selector.
        label (str, optional): The label to use when describing this selector.
        css (Callable[[str], str], optional): A function to generate a CSS selector given a locator
            string.
        xpath (Callable[[str], str], optional): A function to generate an XPath query given a
            locator string.
    """

    def __init__(self, name, label=None, css=None, xpath=None):
        self.name = name
        self.label = label
        self.css = css
        self.xpath = xpath
        self.format = "xpath" if xpath else "css"

    def __call__(self, locator):
        assert self.format, "selector has no format"
        return getattr(self, self.format)(locator)


class SelectorFactory(object):
    """
    A factory for configuring and building :class:`Selector` instances.

    Args:
        name (str): The name of the selector.
    """

    def __init__(self, name):
        self.name = name
        self.label = None
        self.func = None
        self.format = None

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

    def build_selector(self):
        """ Selector: Returns a new :class:`Selector` instance with the current configuration. """

        kwargs = {'label': self.label}
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
