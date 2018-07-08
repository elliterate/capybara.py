import re

from capybara.compat import cmp
from capybara.helpers import declension, desc, failure_message
from capybara.utils import cached_property


class Result(object):
    """
    A :class:`Result` represents a collection of :class:`Element` objects on the page. It is
    possible to interact with this collection similar to a List because it implements
    ``__getitem__`` and offers the following container methods through delegation:

    * ``__len__``
    * ``__nonzero__`` (Python 2)

    Args:
        elements (List[Element]): The initial list of elements found by the query.
        query (SelectorQuery): The query used to find elements.
    """

    def __init__(self, elements, query):
        self._elements = elements

        self._result_cache = []
        self._result_iter = (node for node in elements
                             if query.matches_filters(node))

        self.query = query

    def __getitem__(self, key):
        max_index = key.stop if isinstance(key, slice) else key

        if max_index is None or max_index < 0:
            return self._full_results[key]
        else:
            self._cache_at_least(max_index + 1)
            return self._result_cache[key]

    def __len__(self):
        return len(self._full_results)

    def __nonzero__(self):
        return self._cache_at_least(1)

    def __iter__(self):
        for node in self._result_cache:
            yield node
        for node in self._result_iter:
            self._result_cache.append(node)
            yield node

    @property
    def compare_count(self):
        """
        Returns how the result count compares to the query options.

        The return value is negative if too few results were found, zero if enough were found, and
        positive if too many were found.

        Returns:
            int: -1, 0, or 1.
        """

        if self.query.options["count"] is not None:
            count_opt = int(self.query.options["count"])
            self._cache_at_least(count_opt + 1)
            return cmp(len(self._result_cache), count_opt)

        if self.query.options["minimum"] is not None:
            min_opt = int(self.query.options["minimum"])
            if not self._cache_at_least(min_opt):
                return -1

        if self.query.options["maximum"] is not None:
            max_opt = int(self.query.options["maximum"])
            if self._cache_at_least(max_opt + 1):
                return 1

        if self.query.options["between"] is not None:
            between = self.query.options["between"]
            min_opt, max_opt = between[0], between[-1]
            if not self._cache_at_least(min_opt):
                return -1
            if self._cache_at_least(max_opt + 1):
                return 1
            return 0

        return 0

    @property
    def matches_count(self):
        """ bool: Whether the result count matches the query options. """
        return self.compare_count == 0

    @property
    def failure_message(self):
        """ str: A message describing the query failure. """

        message = failure_message(self.query.description, self.query.options)

        if len(self) > 0:
            message += ", found {count} {matches}: {results}".format(
                count=len(self),
                matches=declension("match", "matches", len(self)),
                results=", ".join([desc(node.text) for node in self]))
        else:
            message += " but there were no matches"

        if self._rest:
            elements = ", ".join([desc(element.text) for element in self._rest])
            message += (". Also found {}, which matched the selector"
                        " but not all filters.".format(elements))

        return message

    @property
    def negative_failure_message(self):
        return re.sub(r"(to find)", r"not \1", self.failure_message)

    def _cache_at_least(self, size):
        """
        Attempts to fill the result cache with at least the given number of results.

        Returns:
            bool: Whether the cache contains at least the given size.
        """

        try:
            while len(self._result_cache) < size:
                self._result_cache.append(next(self._result_iter))
            return True
        except StopIteration:
            return False

    @cached_property
    def _full_results(self):
        return list(iter(self))

    @cached_property
    def _rest(self):
        return list(set(self._elements) - set(self._full_results))
