class Window(object):
    """
    The Window class represents a browser window.

    You can get an instance of the class by calling either of:

    * :attr:`windows`
    * :attr:`current_window`
    * :meth:`window_opened_by`
    * :meth:`switch_to_window`

    Note that some drivers (e.g. Selenium) support getting size of/resizing/closing only current
    window. So if you invoke such method for:

    * window that is current, Capybara will make 2 Selenium method invocations (get handle of
      current window + get size/resize/close).
    * window that is not current, Capybara will make 4 Selenium method invocations (get handle of
      current window + switch to given handle + get size/resize/close + switch to original handle)

    Args:
        session (Session): Session that this window belongs to.
        handle (object): An object that uniquely identifies the window within the session.
    """

    def __init__(self, session, handle):
        self.session = session
        self.driver = session.driver
        self.handle = handle

    def __repr__(self):
        return "<capybara.window.Window handle={}>".format(repr(self.handle))

    def __eq__(self, other):
        return (
            type(self) == type(other) and
            self.session == other.session and
            self.handle == other.handle)

    def __hash__(self):
        return hash(self.session) ^ hash(self.handle)

    @property
    def closed(self):
        """ bool: Whether the window is closed. """
        return not self.exists

    @property
    def current(self):
        """ bool: Whether this window is the window in which commands are being executed. """
        try:
            return self.driver.current_window_handle == self.handle
        except self.driver.no_such_window_error:
            return False

    @property
    def exists(self):
        """ bool: Whether the window is not closed. """
        return self.handle in self.driver.window_handles

    @property
    def size(self):
        """ List[int, int]: The window size. """
        return self.driver.window_size(self.handle)

    def close(self):
        """
        Close window.

        If this method was called for the window that is current, then after calling this method
        future invocations of other Capybara methods should raise
        ``session.driver.no_such_window_error`` until another window is switched to.

        If this method was called for a window that is not current, then after calling this method
        the current window should remain the same as it was before calling this method.
        """

        self.driver.close_window(self.handle)

    def maximize(self):
        """
        Maximize the window.

        If this method was called for a window that is not current, then after calling this method
        the current window should remain the same as it was before calling this method.
        """

        self.driver.maximize_window(self.handle)

    def resize_to(self, width, height):
        """
        Resizes the window to the given dimensions.

        If this method was called for a window that is not current, then after calling this method
        the current window should remain the same as it was before calling this method.

        Args:
            width (int): The new window width in pixels.
            height (int): The new window height in pixels.
        """

        self.driver.resize_window_to(self.handle, width, height)
