import re

import capybara
from capybara.helpers import declension, desc, failure_message, normalize_text


VALID_QUERY_TYPE = ["all", "visible"]


class TextQuery(object):
    """
    Queries for text content in a node.

    If only one argument is provided, it will be assumed to be ``expected_text``.

    Args:
        query_type (str, optional): One of "visible" or "all". Defaults to "visible".
        expected_text (str): The desired text.
        count (int, optional): The number of times the text should match. Defaults to any number of
            times greater than zero.
    """

    def __init__(self, query_type, expected_text=None, count=None):
        if expected_text is None:
            expected_text = query_type
            query_type = None

        if query_type is None:
            query_type = ("visible" if capybara.ignore_hidden_elements or capybara.visible_text_only
                          else "all")

        assert query_type in VALID_QUERY_TYPE, \
            "invalid option {query_type} for query_type, should be one of {valid_values}".format(
                query_type=desc(query_type),
                valid_values=", ".join(desc(VALID_QUERY_TYPE)))

        self.expected_text = normalize_text(expected_text)
        self.query_type = query_type
        self.search_regexp = re.compile(re.escape(self.expected_text))
        self.options = {
            "count": count}
        self.node = None
        self.actual_text = None
        self.count = None

    def resolve_for(self, node):
        """
        Resolves this query relative to the given node.

        Args:
            node (node.Base): The node to be evaluated.

        Returns:
            int: The number of matches found.
        """

        self.node = node
        self.actual_text = normalize_text(
            node.visible_text if self.query_type == "visible" else node.all_text)
        self.count = len(re.findall(self.search_regexp, self.actual_text))

        return self.count

    @property
    def failure_message(self):
        """ str: A message describing the query failure. """

        description = "text {expected}".format(expected=desc(self.expected_text))

        message = failure_message(description, self.options)
        message += " in {actual}".format(actual=desc(self.actual_text))

        details_message = []

        if self.node and not self.search_regexp.flags & re.IGNORECASE:
            insensitive_regex = re.compile(
                self.search_regexp.pattern,
                flags=(self.search_regexp.flags | re.IGNORECASE))
            insensitive_count = len(re.findall(insensitive_regex, self.actual_text))
            if insensitive_count != self.count:
                details_message.append(
                    "it was found {count} {times} using a case insensitive search".format(
                        count=insensitive_count,
                        times=declension("time", "times", insensitive_count)))

        if self.node and self.query_type == "visible":
            invisible_text = normalize_text(self.node.all_text)
            invisible_count = len(re.findall(self.search_regexp, invisible_text))
            if invisible_count != self.count:
                details_message.append(
                    "it was found {count} {times} including non-visible text".format(
                        count=invisible_count,
                        times=declension("time", "times", invisible_count)))

        if details_message:
            message += ". (However, {details}.)".format(details=" and ".join(details_message))

        return message
