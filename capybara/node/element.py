from capybara.node.base import Base


class Element(Base):
    """
    An :class:`Element` represents a single element on the page and has access to HTML attributes
    and other properties of the element::

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
