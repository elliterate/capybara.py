from capybara.helpers import desc, failure_message, normalize_text


VALID_QUERY_TYPE = ["all", "visible"]


class TextQuery(object):
    """
    Queries for text content in a node.

    If only one argument is provided, it will be assumed to be ``expected_text``.

    Args:
        query_type (str, optional): One of "visible" or "all". Defaults to "visible".
        expected_text (str): The desired text.
    """

    def __init__(self, query_type, expected_text=None):
        if expected_text is None:
            expected_text = query_type
            query_type = "visible"

        assert query_type in VALID_QUERY_TYPE, \
            "invalid option {query_type} for query_type, should be one of {valid_values}".format(
                query_type=desc(query_type),
                valid_values=", ".join(desc(VALID_QUERY_TYPE)))

        self.expected_text = normalize_text(expected_text)
        self.query_type = query_type
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
        self.actual_text = normalize_text(
            node.visible_text if self.query_type == "visible" else node.all_text)
        self.matches = self.expected_text in self.actual_text
        return self.matches

    @property
    def failure_message(self):
        """ str: A message describing the query failure. """

        description = "text {expected}".format(expected=desc(self.expected_text))

        message = failure_message(description)
        message += " in {actual}".format(actual=desc(self.actual_text))

        return message
