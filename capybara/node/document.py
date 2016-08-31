from capybara.node.base import Base
from capybara.node.document_matchers import DocumentMatchersMixin


class Document(DocumentMatchersMixin, Base):
    """
    A :class:`Document` represents an HTML document. Any operation performed on it will be
    performed on the entire document.
    """

    def __repr__(self):
        return "<capybara.node.document.Document>"

    @property
    def title(self):
        """ str: The current page title. """
        return self.session.driver.title

    @property
    def text(self):
        """ str: The text of the document. """
        return self.find("xpath", "/html").text

    @property
    def all_text(self):
        """ str: All of the text of the document. """
        return self.find("xpath", "/html").all_text

    @property
    def visible_text(self):
        """ str: Only the visible text of the document. """
        return self.find("xpath", "/html").visible_text
