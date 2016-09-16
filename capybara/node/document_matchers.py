from capybara.exceptions import ExpectationNotMet
from capybara.queries.title_query import TitleQuery


class DocumentMatchersMixin(object):
    def assert_title(self, title):
        """
        Asserts that the page has the given title.

        Args:
            title (str | RegexObject): The string or regex that the title should match.

        Returns:
            True

        Raises:
            ExpectationNotMet: If the assertion hasn't succeeded during the wait time.
        """

        query = TitleQuery(title)

        @self.synchronize
        def assert_title():
            if not query.resolves_for(self):
                raise ExpectationNotMet(query.failure_message)

            return True

        return assert_title()

    def assert_no_title(self, title):
        """
        Asserts that the page doesn't have the given title.

        Args:
            title (str | RegexObject): The string that the title should include.

        Returns:
            True

        Raises:
            ExpectationNotMet: If the assertion hasn't succeeded during the wait time.
        """

        query = TitleQuery(title)

        @self.synchronize
        def assert_no_title():
            if query.resolves_for(self):
                raise ExpectationNotMet(query.negative_failure_message)

            return True

        return assert_no_title()

    def has_title(self, title):
        """
        Checks if the page has the given title.

        Args:
            title (str | RegexObject): The string or regex that the title should match.

        Returns:
            bool: Whether it matches.
        """

        try:
            self.assert_title(title)
            return True
        except ExpectationNotMet:
            return False

    def has_no_title(self, title):
        """
        Checks if the page doesn't have the given title.

        Args:
            title (str | RegexObject): The string that the title should include.

        Returns:
            bool: Whether it doesn't match.
        """

        try:
            self.assert_no_title(title)
            return True
        except ExpectationNotMet:
            return False
