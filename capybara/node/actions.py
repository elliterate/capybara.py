import os.path

import capybara
from capybara.exceptions import ElementNotFound, FileNotFound
from capybara.queries.base_query import BaseQuery


class ActionsMixin(object):
    """
    If the driver is capable of executing JavaScript, actions will wait for a set amount of time and
    continuously retry finding the element until either the element is found or the time expires.
    The length of time :meth:`find` will wait is controlled through
    :data:`capybara.default_max_wait_time`.
    """

    def attach_file(self, locator_or_path, path=None, **kwargs):
        """
        Find a file field on the page and attach a file given its path. The file field can be found
        via its name, id, or label text. ::

            page.attach_file(locator, "/path/to/file.png")

        Args:
            locator_or_path (str): Which field to attach the file to, or the path of the file that
                will be attached.
            path (str, optional): The path of the file that will be attached. Defaults to
                ``locator_or_path``.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.

        Raises:
            FileNotFound: No file exists at the given path.
        """

        if path is None:
            locator, path = None, locator_or_path
        else:
            locator = locator_or_path

        if not os.path.isfile(path):
            raise FileNotFound("cannot attach file, {0} does not exist".format(path))

        self.find("file_field", locator, **kwargs).set(path)

    def check(self, locator=None, allow_label_click=None, **kwargs):
        """
        Find a check box and mark it as checked. The check box can be found via name, id, or label
        text. ::

            page.check("German")

        Args:
            locator (str, optional): Which check box to check.
            allow_label_click (bool, optional): Attempt to click the label to toggle state if
                element is non-visible. Defaults to :data:`capybara.automatic_label_click`.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.
        """

        self._check_with_label(
            "checkbox", True, locator=locator, allow_label_click=allow_label_click, **kwargs)

    def choose(self, locator=None, allow_label_click=None, **kwargs):
        """
        Find a radio button and mark it as checked. The radio button can be found via name, id, or
        label text. ::

            page.choose("Male")

        Args:
            locator (str, optional): Which radio button to choose.
            allow_label_click (bool, optional): Attempt to click the label to toggle state if
                element is non-visible. Defaults to :data:`capybara.automatic_label_click`.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.
        """

        self._check_with_label(
            "radio_button", True, locator=locator, allow_label_click=allow_label_click, **kwargs)

    def click_button(self, locator=None, **kwargs):
        """
        Finds a button on the page and clicks it. This can be any ``<input>`` element of type
        submit, reset, image, or button, or it can be any ``<button>`` element. All buttons can be
        found by their id, value, or title. ``<button>`` elements can also be found by their text
        content, and image ``<input>`` elements by their alt attribute.

        Args:
            locator (str, optional): Which button to find.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.
        """

        return self.find("button", locator, **kwargs).click()

    def click_link(self, locator=None, **kwargs):
        """
        Finds a link by id, text, or title and clicks it. Also looks at image alt text inside the
        link.

        Args:
            locator (str, optional): Text, id, title, or nested image's alt attribute.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.
        """

        return self.find("link", locator, **kwargs).click()

    def click_link_or_button(self, locator=None, **kwargs):
        """
        Finds a button or link by id, text or value and clicks it. Also looks at image alt text
        inside the link.

        Args:
            locator (str, optional): Text, id, or value of link or button.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.
        """

        return self.find("link_or_button", locator, **kwargs).click()

    click_on = click_link_or_button
    """ Alias for :meth:`click_link_or_button`. """

    def fill_in(self, locator=None, current_value=None, value=None, fill_options=None, **kwargs):
        """
        Locate a text field or text area and fill it in with the given text. The field can be found
        via its name, id, or label text. ::

            page.fill_in("Name", value="Bob")

        Args:
            locator (str, optional): Which field to fill in.
            current_value (str, optional): The current value of the field.
            value (str, optional): The value to fill in. Defaults to None.
            fill_options (Dict, optional): Driver-specific options regarding how to fill fields.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.
        """

        if current_value is not None:
            kwargs["value"] = current_value

        fill_options = fill_options or {}

        self.find("fillable_field", locator, **kwargs).set(value, **fill_options)

    def select(self, value=None, field=None, **kwargs):
        """
        If the ``field`` argument is present, ``select`` finds a select box on the page and selects
        a particular option from it. Otherwise it finds an option inside the current scope and
        selects it. If the select box is a multiple select, ``select`` can be called multiple times
        to select more than one option. The select box can be found via its name, id, or label text.
        The option can be found by its text. ::

            page.select("March", field="Month")

        Args:
            value (str, optional): Which option to select.
            field (str, optional): The id, name, or label of the select box.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.
        """

        if field:
            self.find("select", field, **kwargs).find("option", value, **kwargs).select_option()
        else:
            self.find("option", value, **kwargs).select_option()

    def uncheck(self, locator=None, allow_label_click=None, **kwargs):
        """
        Find a check box and uncheck it. The check box can be found via name, id, or label text. ::

            page.uncheck("German")

        Args:
            locator (str, optional): Which check box to uncheck.
            allow_label_click (bool, optional): Attempt to click the label to toggle state if
                element is non-visible. Defaults to :data:`capybara.automatic_label_click`.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.
        """

        self._check_with_label(
            "checkbox", False, locator=locator, allow_label_click=allow_label_click, **kwargs)

    def unselect(self, value=None, field=None, **kwargs):
        """
        Find a select box on the page and unselect a particular option from it. If the select box is
        a multiple select, ``unselect`` can be called multiple times to unselect more than one
        option. The select box can be found via its name, id, or label text. ::

            page.unselect("March", field="Month")

        Args:
            value (str, optional): Which option to unselect.
            field (str, optional): The id, name, or label of the select box.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.
        """

        if field:
            self.find("select", field, **kwargs).find("option", value, **kwargs).unselect_option()
        else:
            self.find("option", value, **kwargs).unselect_option()

    def _check_with_label(self, selector, checked, locator=None, allow_label_click=None, visible=None, wait=None,
                          **kwargs):
        """
        Args:
            selector (str): The selector for the type of element that should be checked/unchecked.
            checked (bool): Whether the element should be checked.
            locator (str, optional): Which element to check.
            allow_label_click (bool, optional): Attempt to click the label to toggle state if
                element is non-visible. Defaults to :data:`capybara.automatic_label_click`.
            visible (bool | str, optional): The desired element visibility. Defaults to
                :data:`capybara.ignore_hidden_elements`.
            wait (int | float, optional): The number of seconds to wait to check the element.
                Defaults to :data:`capybara.default_max_wait_time`.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.
        """

        if allow_label_click is None:
            allow_label_click = capybara.automatic_label_click

        @self.synchronize(wait=BaseQuery.normalize_wait(wait))
        def check_with_label():
            try:
                self.find(selector, locator, visible=visible, **kwargs).set(checked)
            except ElementNotFound as e:
                if not allow_label_click:
                    raise
                try:
                    element = self.find(selector, locator, visible="hidden", **kwargs)
                    label = self.find("label", field=element, visible=True)
                    if element.checked != checked:
                        label.click()
                except Exception:
                    raise e

        check_with_label()
