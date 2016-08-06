import re

from capybara.helpers import desc, normalize_text


class TitleQuery(object):
    """
    Queries the title content of a node.

    Args:
        expected_title (str): The desired title.
    """

    def __init__(self, expected_title):
        self.expected_title = normalize_text(expected_title)
        self.actual_title = None
        self.search_regexp = re.compile(re.escape(self.expected_title))

    def resolves_for(self, node):
        """
        Resolves this query relative to the given node.

        Args:
            node (node.Document): The node to be evaluated.

        Returns:
            bool: Whether the given node matches this query.
        """

        self.actual_title = normalize_text(node.title)
        return bool(self.search_regexp.search(self.actual_title))

    @property
    def failure_message(self):
        """ str: A message describing the query failure. """
        return "expected {actual} to include {expected}".format(
            actual=desc(self.actual_title),
            expected=desc(self.expected_title))
