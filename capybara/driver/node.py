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

    def __eq__(self, other):
        raise NotImplementedError()

    def __hash__(self):
        raise NotImplementedError()

    @property
    def tag_name(self):
        """ str: The tag name of the node. """
        raise NotImplementedError()

    @property
    def visible(self):
        """ bool: Whether or not the node is visible. """
        raise NotImplementedError()

    @property
    def value(self):
        """ str: The value of the node. """
        raise NotImplementedError()

    @property
    def selected(self):
        """ bool: Whether this is a selected option node. """
        raise NotImplementedError()

    @property
    def multiple(self):
        """ bool: Whether this is a multi-select node. """
        raise NotImplementedError()

    @property
    def text(self):
        """ str: The text of the node. """
        raise NotImplementedError()

    @property
    def path(self):
        """ str: An XPath expression describing where on the page the node can be found. """
        raise NotImplementedError()

    @property
    def all_text(self):
        """ str: All of the text of the node. """
        raise NotImplementedError()

    @property
    def visible_text(self):
        """ str: Only the visible text of the node. """
        raise NotImplementedError()

    def __getitem__(self, name):
        """
        Returns the value of a given attribute of this node.

        Args:
            name (str): The name of the desired attribute.

        Returns:
            str: The value of the desired attribute.
        """

        raise NotImplementedError()

    def click(self):
        """ Clicks on this node. """
        raise NotImplementedError()

    def double_click(self):
        """ Double-click the node. """
        raise NotImplementedError()

    def drag_to(self, node):
        """
        Drag the element to the given other element. ::

            source = page.find("#foo")
            target = page.find("#bar")
            source.drag_to(target)

        Args:
            node (Element): The element to drag to.
        """

        raise NotImplementedError()

    def hover(self):
        """ Hover on the node. """
        raise NotImplementedError()

    def right_click(self):
        """ Right-click the node. """
        raise NotImplementedError()

    def select_option(self):
        """ Selects this option node. """
        raise NotImplementedError()

    def send_keys(self, *args):
        """
        Send keystrokes to the node.

        Examples::

            from selenium.webdriver.common.keys import Keys

            element.send_keys("foo")                  # => value: "foo"
            element.send_keys("tet", Keys.LEFT, "s")  # => value: "test"

        Args:
            *args: Variable length list of keys to send.
        """

        raise NotImplementedError()

    def set(self, value):
        """
        Sets the value of this node.

        Args:
            value (bool | str): The desired value.
        """

        raise NotImplementedError()

    def unselect_option(self):
        """ Deselects this option node. """
        raise NotImplementedError()

    @property
    def checked(self):
        """ bool: Whether this node is checked. """
        raise NotImplementedError()

    @property
    def selected(self):
        """ bool: Whether this node is selected. """
        raise NotImplementedError()

    @property
    def disabled(self):
        """ bool: Whether this node is disabled. """
        raise NotImplementedError()

    @property
    def readonly(self):
        """ bool: Whether the node is read-only. """
        raise NotImplementedError()
