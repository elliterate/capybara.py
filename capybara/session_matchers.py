from capybara.exceptions import ExpectationNotMet
from capybara.queries.current_path_query import CurrentPathQuery


class SessionMatchersMixin(object):
    def assert_current_path(self, path, **kwargs):
        """
        Asserts that the page has the given path. By default this will compare against the
        path+query portion of the full URL.

        Args:
            path (str | RegexObject): The string or regex that the current "path" should match.
            **kwargs: Arbitrary keyword arguments for :class:`CurrentPathQuery`.

        Returns:
            True

        Raises:
            ExpectationNotMet: If the assertion hasn't succeeded during the wait time.
        """

        query = CurrentPathQuery(path, **kwargs)

        @self.document.synchronize
        def assert_current_path():
            if not query.resolves_for(self):
                raise ExpectationNotMet(query.failure_message)
        assert_current_path()

        return True

    def assert_no_current_path(self, path, **kwargs):
        """
        Asserts that the page doesn't have the given path.

        Args:
            path (str | RegexObject): The string or regex that the current "path" should match.
            **kwargs: Arbitrary keyword arguments for :class:`CurrentPathQuery`.

        Returns:
            True

        Raises:
            ExpectationNotMet: If the assertion hasn't succeeded during the wait time.
        """

        query = CurrentPathQuery(path, **kwargs)

        @self.document.synchronize
        def assert_no_current_path():
            if query.resolves_for(self):
                raise ExpectationNotMet(query.negative_failure_message)

        assert_no_current_path()

        return True

    def has_current_path(self, path, **kwargs):
        """
        Checks if the page has the given path.

        Args:
            path (str | RegexObject): The string or regex that the current "path" should match.
            **kwargs: Arbitrary keyword arguments for :class:`CurrentPathQuery`.

        Returns:
            bool: Whether it matches.
        """

        try:
            return self.assert_current_path(path, **kwargs)
        except ExpectationNotMet:
            return False

    def has_no_current_path(self, path, **kwargs):
        """
        Checks if the page doesn't have the given path.

        Args:
            path (str | RegexObject): The string or regex that the current "path" should match.
            **kwargs: Arbitrary keyword arguments for :class:`CurrentPathQuery`.

        Returns:
            bool: Whether it doesn't match.
        """

        try:
            return self.assert_no_current_path(path, **kwargs)
        except ExpectationNotMet:
            return False
