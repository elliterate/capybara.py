from capybara.helpers import desc, failure_message, normalize_text


class TextQuery(object):
    """
    Queries for text content in a node.

    Args:
        expected_text (str): The desired text.
    """

    def __init__(self, expected_text):
        self.expected_text = normalize_text(expected_text)
        self.node = None
        self.actual_text = None
        self.matches = None

    def resolve_for(self, node):
        """
        Resolves this query relative to the given node.

        Args:
            node (node.Base): The node to be evaluated.

        Returns:
            bool: Whether the given node matches this query.
        """

        self.node = node
        self.actual_text = normalize_text(node.text)
        self.matches = self.expected_text in self.actual_text
        return self.matches

    @property
    def failure_message(self):
        """ str: A message describing the query failure. """

        description = "text {expected}".format(expected=desc(self.expected_text))

        message = failure_message(description)
        message += " in {actual}".format(actual=desc(self.actual_text))

        return message
