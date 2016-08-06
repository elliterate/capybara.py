from capybara.node.base import Base


class Element(Base):
    """
    An :class:`Element` represents a single element on the page and has access to properties of the
    element::

        bar.text
    """

    def __repr__(self):
        return "<capybara.node.element.Element tag=\"{tag}\">".format(
            tag=self.tag_name)

    @property
    def tag_name(self):
        """ str: The tag name of the element. """
        return self.base.tag_name

    @property
    def text(self):
        """ str: The text of the element. """
        return self.base.text
