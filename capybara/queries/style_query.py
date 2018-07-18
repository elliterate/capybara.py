from capybara.helpers import desc, toregex
from capybara.queries.base_query import BaseQuery


class StyleQuery(BaseQuery):
    """
    Queries for computed style values of a node.

    Args:
        expected_styles (Dict[str, str]): The expected style names and values.
        wait (bool | int | float, optional): Whether and how long to wait for synchronization.
            Defaults to :data:`capybara.default_max_wait_time`.
    """

    def __init__(self, expected_styles, wait=None):
        self.expected_styles = expected_styles
        self.actual_styles = {}
        self.options = {
            "wait": wait}
        self.node = None

    @property
    def wait(self):
        """ int | float: How long to wait for synchronization. """
        return self.normalize_wait(self.options["wait"])

    def resolves_for(self, node):
        """
        Resolves this query relative to the given node.

        Args:
            node (node.Base): The node to be evaluated.

        Returns:
            int: The number of matches found.
        """

        self.node = node
        self.actual_styles = node.style(*self.expected_styles.keys())

        return all(
            toregex(value).search(self.actual_styles[style])
            for style, value in iter(self.expected_styles.items()))

    @property
    def failure_message(self):
        """ str: A message describing the query failure. """
        return (
            "Expected node to have styles {expected}. "
            "Actual styles were {actual}").format(
                expected=desc(self.expected_styles),
                actual=desc(self.actual_styles))
