from capybara.exceptions import ExpectationNotMet
from capybara.queries.title_query import TitleQuery


class DocumentMatchersMixin(object):
    def assert_title(self, title):
        """
        Asserts that the page has the given title.

        Args:
            title (str): The string that the title should include.

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

    def has_title(self, title):
        """
        Checks if the page has the given title.

        Args:
            title (str): The string that the title should include.

        Returns:
            bool: Whether it matches.
        """

        try:
            self.assert_title(title)
            return True
        except ExpectationNotMet:
            return False
