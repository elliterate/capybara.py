import sys
if sys.version_info >= (3, 0):
    from urllib.parse import urlparse
else:
    from urlparse import urlparse

from capybara.helpers import desc
from capybara.utils import isregex


class CurrentPathQuery(object):
    """
    Queries the current path.

    Args:
        expected_path (str | RegexObject): The expected path.
        url (bool, optional): Whether the complete URL should match. Defaults to False.
        only_path (bool, optional): Whether only the path (excluding the query string) should
            match. Defaults to False.
    """

    def __init__(self, expected_path, url=False, only_path=False):
        if url and only_path:
            raise RuntimeError("the url and only_path arguments cannot both be true")

        self.expected_path = expected_path
        self.actual_path = None
        self.url = url
        self.only_path = only_path

    def resolves_for(self, session):
        """
        Returns whether this query resolves for the given session.

        Args:
            session (Session): The session for which this query should be executed.

        Returns:
            bool: Whether this query resolves.
        """

        if self.url:
            self.actual_path = session.current_url
        else:
            result = urlparse(session.current_url)

            if self.only_path:
                self.actual_path = result.path
            else:
                request_uri = result.path
                if result.query:
                    request_uri += "?{0}".format(result.query)

                self.actual_path = request_uri

        if isregex(self.expected_path):
            return self.expected_path.search(self.actual_path)
        else:
            return self.actual_path == self.expected_path

    @property
    def failure_message(self):
        """ str: A description of this query's failure. """
        return self._build_message()

    @property
    def negative_failure_message(self):
        """ str: A description of this query's negative failure. """
        return self._build_message(" not")

    def _build_message(self, negated=""):
        verb = "match" if isregex(self.expected_path) else "equal"

        return "expected {actual}{negated} to {verb} {expected}".format(
            actual=desc(self.actual_path),
            negated=negated,
            verb=verb,
            expected=desc(self.expected_path))
