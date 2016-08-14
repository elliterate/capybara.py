from contextlib import contextmanager


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

    def switch_to_frame(self, frame):
        """
        Switch to the given frame.

        Args:
            frame (Element | str): The element of the desired frame, or "parent".
        """

        raise NotImplementedError()

    def visit(self, path):
        """
        Visits the given path.

        Args:
            path (str): The path to visit.
        """

        raise NotImplementedError()

    @contextmanager
    def accept_modal(self, modal_type, text=None, wait=None):
        """
        Accepts the modal that appears matching the given type and, optionally, text.

        Args:
            modal_type (str): The type of modal that should be accepted.
            text (str, optional): Text that is expected to appear in the modal.
            wait (int, optional): The number of seconds to wait for the modal to appear.
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
