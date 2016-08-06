from capybara.node.base import Base


class Document(Base):
    """
    A :class:`Document` represents an HTML document. Any operation performed on it will be
    performed on the entire document.
    """

    def __repr__(self):
        return "<capybara.node.document.Document>"

    @property
    def text(self):
        """ str: The text of the document. """
        return self.find("xpath", "/html").text
