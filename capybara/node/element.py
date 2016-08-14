from capybara.node.base import Base


class Element(Base):
    """
    An :class:`Element` represents a single element on the page. It is possible to interact with the
    contents of this element the same as with a document::

        session = Session("selenium", my_app)

        bar = session.find("#bar")       # from capybara.node.finders.FindersMixin
        bar.select("Baz", field="Quox")  # from capybara.node.actions.ActionsMixin

    :class:`Element` also has access to HTML attributes and other properties of the element::

        bar.value
        bar.text
        bar["title"]
    """

    def __repr__(self):
        return "<capybara.node.element.Element tag=\"{tag}\">".format(
            tag=self.tag_name)

    @property
    def native(self):
        """ object: The native element from the driver. """
        return self.base.native

    @property
    def tag_name(self):
        """ str: The tag name of the element. """
        return self.base.tag_name

    @property
    def value(self):
        """ str: The value of the form element. """
        return self.base.value

    @property
    def text(self):
        """ str: The text of the element. """
        return self.base.text

    @property
    def checked(self):
        """ bool: Whether or not the element is checked. """
        return self.base.checked

    @property
    def selected(self):
        """ bool: Whether or not the element is selected. """
        return self.base.selected

    def __getitem__(self, name):
        """
        Retrieve the given attribute. ::

            element["title"]  # => HTML title attribute

        Args:
            name (str): The attribute to retrieve.

        Returns:
            str: The value of the attribute.
        """

        return self.base[name]

    def click(self):
        """ Click the element. """
        self.base.click()

    def select_option(self):
        """ Select this node if it is an option element inside a select tag. """
        self.base.select_option()

    def set(self, value):
        """
        Set the value of the form element to the given value.

        Args:
            value (bool | str): The new value.
        """

        self.base.set(value)

    def unselect_option(self):
        """ Unselect this node if it is an option element inside a multiple select tag. """
        self.base.unselect_option()
