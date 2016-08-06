class Base(object):
    """ The base class for drivers used by sessions. """

    def visit(self, path):
        """
        Visits the given path.

        Args:
            path (str): The path to visit.
        """

        raise NotImplementedError()

    def _find_xpath(self, query):
        """
        A private method for finding nodes matching a given XPath query.

        Args:
            query (str): The XPath query to match.

        Returns:
            List[driver.Node]: A list of matching nodes found by the driver.
        """

        raise NotImplementedError()
