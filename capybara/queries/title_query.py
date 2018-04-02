import re

import capybara
from capybara.helpers import desc, normalize_text, toregex
from capybara.utils import isregex


class TitleQuery(object):
    """
    Queries the title content of a node.

    Args:
        expected_title (str | RegexObject): The desired title.
        exact (bool, optional): Whether the text should match exactly. Defaults to False.
        wait (bool | int | float, optional): Whether and how long to wait for synchronization.
            Defaults to :data:`capybara.default_max_wait_time`.
    """

    def __init__(self, expected_title, exact=False, wait=None):
        self.expected_title = (expected_title if isregex(expected_title)
                               else normalize_text(expected_title))
        self.actual_title = None
        self.search_regexp = toregex(expected_title, exact=exact)

        self.options = {
            "wait": wait}

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
    def wait(self):
        """ int | float: How long to wait for synchronization. """
        if self.options["wait"] is not None:
            return self.options["wait"] or 0
        else:
            return capybara.default_max_wait_time

    @property
    def failure_message(self):
        """ str: A message describing the query failure. """
        return self._build_message()

    @property
    def negative_failure_message(self):
        """ str: A message describing the negative query failure. """
        return self._build_message(" not")

    def _build_message(self, negated=""):
        verb = "match" if isregex(self.expected_title) else "include"
        return "expected {actual}{negated} to {verb} {expected}".format(
            actual=desc(self.actual_title),
            negated=negated,
            verb=verb,
            expected=desc(self.expected_title))
