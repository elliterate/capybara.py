import os.path

from capybara.exceptions import FileNotFound


class ActionsMixin(object):
    """
    If the driver is capable of executing JavaScript, actions will wait for a set amount of time and
    continuously retry finding the element until either the element is found or the time expires.
    The length of time :meth:`find` will wait is controlled through
    :data:`capybara.default_max_wait_time`.
    """

    def attach_file(self, locator, path, **kwargs):
        """
        Find a file field on the page and attach a file given its path. The file field can be found
        via its name, id, or label text. ::

            session.attach_file(locator, "/path/to/file.png")

        Args:
            locator (str): Which field to attach the file to.
            path (str): The path of the file that will be attached.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.

        Raises:
            FileNotFound: No file exists at the given path.
        """

        if not os.path.isfile(path):
            raise FileNotFound("cannot attach file, {0} does not exist".format(path))

        self.find("file_field", locator, **kwargs).set(path)

    def check(self, locator, **kwargs):
        """
        Find a check box and mark it as checked. The check box can be found via name, id, or label
        text. ::

            session.check("German")

        Args:
            locator (str): Which check box to check.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.
        """

        self.find("checkbox", locator, **kwargs).set(True)

    def choose(self, locator, **kwargs):
        """
        Find a radio button and mark it as checked. The radio button can be found via name, id, or
        label text. ::

            session.choose("Male")

        Args:
            locator (str): Which radio button to choose.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.
        """

        self.find("radio_button", locator, **kwargs).set(True)

    def click_button(self, locator, **kwargs):
        """
        Finds a button on the page and clicks it. This can be any ``<input>`` element of type
        submit, reset, image, or button, or it can be any ``<button>`` element. All buttons can be
        found by their id, value, or title. ``<button>`` elements can also be found by their text
        content, and image ``<input>`` elements by their alt attribute.

        Args:
            locator (str): Which button to find.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.
        """

        return self.find("button", locator, **kwargs).click()

    def click_link(self, locator, **kwargs):
        """
        Finds a link by id, text, or title and clicks it. Also looks at image alt text inside the
        link.

        Args:
            locator (str): Text, id, title, or nested image's alt attribute.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.
        """

        return self.find("link", locator, **kwargs).click()

    def click_link_or_button(self, locator, **kwargs):
        """
        Finds a button or link by id, text or value and clicks it. Also looks at image alt text
        inside the link.

        Args:
            locator (str): Text, id, or value of link or button.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.
        """

        return self.find("link_or_button", locator, **kwargs).click()

    click_on = click_link_or_button
    """ Alias for :meth:`click_link_or_button`. """

    def fill_in(self, locator, value=None, **kwargs):
        """
        Locate a text field or text area and fill it in with the given text. The field can be found
        via its name, id, or label text. ::

            page.fill_in("Name", value="Bob")

        Args:
            locator (str): Which field to fill in.
            value (str, optional): The value to fill in. Defaults to None.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.
        """

        self.find("fillable_field", locator, **kwargs).set(value)

    def select(self, value, field=None, **kwargs):
        """
        If the ``field`` argument is present, ``select`` finds a select box on the page and selects
        a particular option from it. Otherwise it finds an option inside the current scope and
        selects it. If the select box is a multiple select, ``select`` can be called multiple times
        to select more than one option. The select box can be found via its name, id, or label text.
        The option can be found by its text. ::

            session.select("March", field="Month")

        Args:
            value (str): Which option to select.
            field (str, optional): The id, name, or label of the select box.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.
        """

        if field:
            self.find("select", field, **kwargs).find("option", value, **kwargs).select_option()
        else:
            self.find("option", value, **kwargs).select_option()

    def uncheck(self, locator, **kwargs):
        """
        Find a check box and uncheck it. The check box can be found via name, id, or label text. ::

            session.uncheck("German")

        Args:
            locator (str): Which check box to uncheck.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.
        """

        self.find("checkbox", locator, **kwargs).set(False)

    def unselect(self, value, field=None, **kwargs):
        """
        Find a select box on the page and unselect a particular option from it. If the select box is
        a multiple select, ``unselect`` can be called multiple times to unselect more than one
        option. The select box can be found via its name, id, or label text. ::

            session.unselect("March", field="Month")

        Args:
            value (str): Which option to unselect.
            field (str, optional): The id, name, or label of the select box.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.
        """

        if field:
            self.find("select", field, **kwargs).find("option", value, **kwargs).unselect_option()
        else:
            self.find("option", value, **kwargs).unselect_option()
