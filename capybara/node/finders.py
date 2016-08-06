from capybara.exceptions import ElementNotFound
from capybara.queries.selector_query import SelectorQuery


class FindersMixin(object):
    def find(self, *args, **kwargs):
        """
        Find an :class:`Element` based on the given arguments. ``find`` will raise an error if the
        element is not found. ::

            page.find("xpath", "//div[contains(., 'bar')]")

        Args:
            *args: Variable length argument list for :class:`SelectorQuery`.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.

        Returns:
            Element: The found element.

        Raises:
            ElementNotFound: If the element can't be found.
        """

        query = SelectorQuery(*args, **kwargs)
        result = query.resolve_for(self)

        if len(result) == 0:
            raise ElementNotFound("Unable to find {0}".format(query.description))

        return result[0]

    def find_link(self, locator, **kwargs):
        """
        Find a link on the page. The link can be found by its id or text.

        Args:
            locator (str): ID, title, text, or alt of enclosed img element.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.

        Returns:
            Element: The found element.
        """

        return self.find("link", locator, **kwargs)
