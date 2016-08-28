from capybara.exceptions import Ambiguous, ElementNotFound
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
        element is not found.

        ``find`` takes the same options as :meth:`find_all`. ::

            page.find("#foo").find(".bar")
            page.find("xpath", "//div[contains(., 'bar')]")
            page.find("li").click_link("Delete")

        Args:
            *args: Variable length argument list for :class:`SelectorQuery`.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.

        Returns:
            Element: The found element.

        Raises:
            Ambiguous: If more than one element matching element is found.
            ElementNotFound: If the element can't be found before time expires.
        """

        query = SelectorQuery(*args, **kwargs)

        @self.synchronize
        def find():
            result = query.resolve_for(self)

            if len(result) > 1:
                raise Ambiguous("Ambiguous match, found {count} elements matching {query}".format(
                    count=len(result), query=query.description))
            if len(result) == 0:
                raise ElementNotFound("Unable to find {0}".format(query.description))

            element = result[0]
            element.allow_reload = True
            return element

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

    def find_all(self, *args, **kwargs):
        """
        Find all elements on the page matching the given selector and options.

        Both XPath and CSS expressions are supported, but Capybara does not try to automatically
        distinguish between them. The following statements are equivalent::

            session.find_all("css", "a#person_123")
            session.find_all("xpath", "//a[@id='person_123']")

        If the type of selector is left out, Capybara uses :data:`capybara.default_selector`. It's
        set to ``"css"`` by default. ::

            session.find_all("a#person_123")

            capybara.default_selector = "xpath"
            session.find_all("//a[@id='person_123']")

        Args:
            *args: Variable length argument list for :class:`SelectorQuery`.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.

        Returns:
            Result: A collection of found elements.
        """

        query = SelectorQuery(*args, **kwargs)

        @self.synchronize
        def find_all():
            return query.resolve_for(self)

        return find_all()

    def find_first(self, *args, **kwargs):
        """
        Find the first element on the page matching the given selector and options, or None if no
        element matches.

        Args:
            *args: Variable length argument list for :class:`SelectorQuery`.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.

        Returns:
            Element: The found element or None.
        """

        result = self.find_all(*args, **kwargs)
        return result[0] if len(result) > 0 else None
