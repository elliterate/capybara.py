from capybara.exceptions import ElementNotFound
from capybara.queries.selector_query import SelectorQuery


class FindersMixin(object):
    """
    If the driver is capable of executing JavaScript, finders will wait for a set amount of time and
    continuously retry finding the element until either the element is found or the time expires.
    The length of time :meth:`find` will wait is controlled through
    :data:`capybara.default_max_wait_time` and defaults to 2 seconds.
    """

    def find(self, *args, **kwargs):
        """
        Find an :class:`Element` based on the given arguments. ``find`` will raise an error if the
        element is not found. ::

            page.find("#foo").find(".bar")
            page.find("xpath", "//div[contains(., 'bar')]")
            page.find("li").click_link("Delete")

        Args:
            *args: Variable length argument list for :class:`SelectorQuery`.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.

        Returns:
            Element: The found element.

        Raises:
            ElementNotFound: If the element can't be found before time expires.
        """

        query = SelectorQuery(*args, **kwargs)

        @self.synchronize
        def find():
            result = query.resolve_for(self)

            if len(result) == 0:
                raise ElementNotFound("Unable to find {0}".format(query.description))

            return result[0]

        return find()

    def find_button(self, locator, **kwargs):
        """
        Find a button on the page. This can be any ``<input>`` element of type submit, reset, image,
        or button, or it can be a ``<button>`` element. All buttons can be found by their id, value,
        or title. ``<button>`` elements can also be found by their text content, and image
        ``<input>`` elements by their alt attribute.

        Args:
            locator (str): The id, value, title, text content, alt of image.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.

        Returns:
            Element: The found element.
        """

        return self.find("button", locator, **kwargs)

    def find_by_id(self, id, **kwargs):
        """
        Find an element on the page, given its id.

        Args:
            id (str): The id of the element.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.

        Returns:
            Element: The found element.
        """

        return self.find("id", id, **kwargs)

    def find_field(self, locator, **kwargs):
        """
        Find a form field on the page. The field can be found by its name, id, or label text.

        Args:
            locator (str): Name, id, placeholder, or text of associated label element.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.

        Returns:
            Element: The found element.
        """

        return self.find("field", locator, **kwargs)

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
