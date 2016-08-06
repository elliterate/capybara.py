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
        xpath (Callable[[str], str], optional): A function to generate an XPath query given a
            locator string.
    """

    def __init__(self, name, label=None, xpath=None):
        """
        """

        self.name = name
        self.label = label
        self.xpath = xpath

    def __call__(self, locator):
        return self.xpath(locator)


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

    @setter_decorator
    def xpath(self, func):
        """
        Sets the given function as the XPath query generation function.

        Args:
            func (Callable[[str], str]): The XPath query generation function.
        """

        self.func = func

    def build_selector(self):
        """ Selector: Returns a new :class:`Selector` instance with the current configuration. """
        kwargs = {'label': self.label, 'xpath': self.func}
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
