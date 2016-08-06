from capybara.exceptions import ExpectationNotMet
from capybara.queries.text_query import TextQuery


class MatchersMixin(object):
    def assert_text(self, *args, **kwargs):
        """
        Asserts that the page or current node has the given text content, ignoring any HTML tags.

        Args:
            *args: Variable length argument list for :class:`TextQuery`.
            **kwargs: Arbitrary keyword arguments for :class:`TextQuery`.

        Returns:
            True

        Raises:
            ExpectationNotMet: If the assertion hasn't succeeded during the wait time.
        """

        query = TextQuery(*args, **kwargs)
        matches = query.resolve_for(self)

        if not matches:
            raise ExpectationNotMet(query.failure_message)

        return True

    def has_text(self, *args, **kwargs):
        """
        Checks if the page or current node has the given text content, ignoring any HTML tags.

        Whitespaces are normalized in both the node's text and the passed text parameter.

        Args:
            *args: Variable length argument list for :class:`TextQuery`.
            **kwargs: Arbitrary keyword arguments for :class:`TextQuery`.

        Returns:
            bool: Whether it exists.
        """

        try:
            return self.assert_text(*args, **kwargs)
        except ExpectationNotMet:
            return False

    has_content = has_text
    """ Alias for :meth:`has_text`. """
