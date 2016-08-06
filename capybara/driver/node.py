class Node(object):
    """
    The base class for nodes returned by a driver.

    Args:
        driver (driver.Base): The driver used to find this node.
        native (object): The native element object returned by the driver's browser.
    """

    def __init__(self, driver, native):
        self.driver = driver
        self.native = native

    @property
    def tag_name(self):
        """ str: The tag name of the node. """
        raise NotImplementedError()

    @property
    def text(self):
        """ str: The text of the node. """
        raise NotImplementedError()
