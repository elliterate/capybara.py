import re

import capybara
from capybara.helpers import declension, desc, failure_message, normalize_text, toregex
from capybara.utils import isregex


VALID_QUERY_TYPE = ["all", "visible"]


class TextQuery(object):
    """
    Queries for text content in a node.

    If only one argument is provided, it will be assumed to be ``expected_text``.

    Args:
        query_type (str, optional): One of "visible" or "all". Defaults to "visible".
        expected_text (str | RegexObject): The desired text.
        between (Iterable[int], optional): A range of acceptable counts.
        count (int, optional): The number of times the text should match. Defaults to any number of
            times greater than zero.
        maximum (int, optional): The maximum number of times the selector should match. Defaults to
            infinite.
        minimum (int, optional): The minimum number of times the selector should match. Defaults to
            1.
        wait (bool | int | float, optional): Whether and how long to wait for synchronization.
            Defaults to :data:`capybara.default_max_wait_time`.
    """

    def __init__(self, query_type, expected_text=None, between=None, count=None, maximum=None,
                 minimum=None, wait=None):
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

        self.expected_text = (expected_text if isregex(expected_text)
                              else normalize_text(expected_text))
        self.query_type = query_type
        self.search_regexp = toregex(expected_text)
        self.options = {
            "between": between,
            "count": count,
            "maximum": maximum,
            "minimum": minimum,
            "wait": wait}
        self.node = None
        self.actual_text = None
        self.count = None

    @property
    def wait(self):
        """ int | float: How long to wait for synchronization. """
        if self.options["wait"] is not None:
            return self.options["wait"] or 0
        else:
            return capybara.default_max_wait_time

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
    def description(self):
        if isregex(self.expected_text):
            return "text matching {}".format(desc(self.expected_text))
        else:
            return "text {}".format(desc(self.expected_text))

    @property
    def failure_message(self):
        """ str: A message describing the query failure. """
        return self._build_message(True)

    @property
    def negative_failure_message(self):
        """ str: A message describing the negative query failure. """
        return re.sub(r"(to find)", r"not \1", self._build_message(False))

    def _build_message(self, report_on_invisible):
        message = failure_message(self.description, self.options)
        if any(self.options.values()):
            message += " but found {count} {times}".format(
                count=self.count,
                times=declension("time", "times", self.count))
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

        if self.node and self.query_type == "visible" and report_on_invisible:
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
