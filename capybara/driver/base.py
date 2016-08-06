class Base(object):
    """ The base class for drivers used by sessions. """

    @property
    def title(self):
        """ str: The current page title. """
        raise NotImplementedError()

    @property
    def html(self):
        """ str: A snapshot of the DOM of the current document, as it looks right now. """
        raise NotImplementedError()

    def visit(self, path):
        """
        Visits the given path.

        Args:
            path (str): The path to visit.
        """

        raise NotImplementedError()

    def _find_css(self, query):
        """
        A private method for finding nodes matching a given CSS query.

        Args:
            query (str): The CSS query to match.

        Returns:
            list(driver.Node): A list of matching nodes found by the driver.
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
