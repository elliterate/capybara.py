import re

from capybara.helpers import declension, desc, failure_message


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

        # Further reduce the result set using the query's filters.
        self.result = [node for node in elements
                       if query.matches_filters(node)]
        self.rest = list(set(elements) - set(self.result))
        self.query = query

    def __getitem__(self, key):
        return self.result[key]

    def __len__(self):
        return len(self.result)

    def __nonzero__(self):
        return len(self.result) > 0

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

        if self.rest:
            elements = ", ".join([desc(element.text) for element in self.rest])
            message += (". Also found {}, which matched the selector"
                        " but not all filters.".format(elements))

        return message

    @property
    def negative_failure_message(self):
        return re.sub(r"(to find)", r"not \1", self.failure_message)
