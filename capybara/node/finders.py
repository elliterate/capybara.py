import capybara
from capybara.exceptions import Ambiguous, ElementNotFound, ExpectationNotMet
from capybara.helpers import matches_count
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
            page.find("li", text="Quox").click_link("Delete")

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

        @self.synchronize(wait=query.wait)
        def find():
            if query.match in ["prefer_exact", "smart"]:
                result = query.resolve_for(self, True)
                if len(result) == 0 and not query.exact:
                    result = query.resolve_for(self, False)
            else:
                result = query.resolve_for(self)

            if query.match in ["one", "smart"] and len(result) > 1:
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

            page.find_all("css", "a#person_123")
            page.find_all("xpath", "//a[@id='person_123']")

        If the type of selector is left out, Capybara uses :data:`capybara.default_selector`. It's
        set to ``"css"`` by default. ::

            page.find_all("a#person_123")

            capybara.default_selector = "xpath"
            page.find_all("//a[@id='person_123']")

        The set of found elements can further be restricted by specifying options. It's possible to
        select elements by their text or visibility::

            page.find_all("a", text="Home")
            page.find_all("#menu li", visible=True)

        By default if no elements are found, an empty list is returned; however, expectations can be
        set on the number of elements to be found which will trigger Capybara's waiting behavior for
        the expectations to match. The expectations can be set using::

            page.assert_selector("p#foo", count=4)
            page.assert_selector("p#foo", maximum=10)
            page.assert_selector("p#foo", minimum=1)
            page.assert_selector("p#foo", between=range(1, 11))

        See :func:`matches_count` for additional information about count matching.

        Args:
            *args: Variable length argument list for :class:`SelectorQuery`.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.

        Returns:
            Result: A collection of found elements.

        Raises:
            ExpectationNotMet: The matched results did not meet the expected criteria.
        """

        query = SelectorQuery(*args, **kwargs)

        @self.synchronize(wait=query.wait)
        def find_all():
            result = query.resolve_for(self)

            if not matches_count(len(result), query.options):
                raise ExpectationNotMet(result.failure_message)

            return result

        return find_all()

    def find_first(self, *args, **kwargs):
        """
        Find the first element on the page matching the given selector and options, or None if no
        element matches.

        By default, no waiting behavior occurs. However, if ``capybara.wait_on_first_by_default``
        is set to true, it will trigger Capybara's waiting behavior for a minimum of 1 matching
        element to be found.

        Args:
            *args: Variable length argument list for :class:`SelectorQuery`.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.

        Returns:
            Element: The found element or None.
        """

        if capybara.wait_on_first_by_default:
            kwargs.setdefault("minimum", 1)

        try:
            result = self.find_all(*args, **kwargs)
            return result[0] if len(result) > 0 else None
        except ExpectationNotMet:
            return None
