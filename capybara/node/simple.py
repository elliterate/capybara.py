from xpath import dsl as x
from xpath.renderer import to_xpath

from capybara.node.document_matchers import DocumentMatchersMixin
from capybara.node.finders import FindersMixin
from capybara.node.matchers import MatchersMixin
from capybara.utils import inner_content


class Simple(FindersMixin, MatchersMixin, DocumentMatchersMixin, object):
    """
    A :class:`Simple` is a simpler version of :class:`Base` which includes only
    :class:`FindersMixin` and :class:`MatchersMixin` and does not include :class:`ActionsMixin`.
    This type of node is returned when using :func:`capybara.string`.

    It is useful in that it does not require a session, an application, or a driver, but can still
    use Capybara's finders and matchers on any string that contains HTML.
    """

    def __init__(self, native):
        if isinstance(native, str):
            from lxml import etree
            native = etree.HTML(native)
        self.native = native

    def __getitem__(self, name):
        """
        Return the given attribute. ::

            element["title"]  # => HTML title attribute

        Args:
            name (str): The attribute name to retrieve.

        Returns:
            str: The value of the attribute.
        """

        return self.native.get(name)

    @property
    def tag_name(self):
        """ str: The tag name of the element. """
        return self.native.tag

    @property
    def path(self):
        """ str: An XPath expression describing where on the page the element can be found. """
        return self.native.getroottree().getpath(self.native)

    @property
    def text(self):
        """ str: The text of the element. """
        return self.native.text

    @property
    def value(self):
        """ str: The value of the form element. """

        if self.tag_name == "textarea":
            return inner_content(self.native)
        elif self.tag_name == "select":
            if self["multiple"] == "multiple":
                selected_options = self._find_xpath(".//option[@selected='selected']")
                return [_get_option_value(option) for option in selected_options]
            else:
                options = (
                    self._find_xpath(".//option[@selected='selected']") +
                    self._find_xpath(".//option"))
                return _get_option_value(options[0]) if options else None
        elif self.tag_name == "input" and self["type"] in ["checkbox", "radio"]:
            return self["value"] or "on"
        else:
            return self["value"]

    @property
    def visible(self):
        """ bool: Whether or not the element is visible. """

        if self.tag_name == "input" and self.native.get("type") == "hidden":
            return False

        return not self.native.xpath(
            "./ancestor-or-self::*["
            "contains(@style, 'display:none') or "
            "contains(@style, 'display: none') or "
            "@hidden or "
            "name()='script' or "
            "name()='head'"
            "]")

    @property
    def checked(self):
        """ bool: Whether or not the element is checked. """
        return "checked" in self.native.attrib

    @property
    def disabled(self):
        """ bool: Whether or not the element is disabled. """
        return "disabled" in self.native.attrib

    @property
    def selected(self):
        """ bool: Whether or not the element is selected. """
        return "selected" in self.native.attrib

    @property
    def allow_reload(self):
        return False

    @allow_reload.setter
    def allow_reload(self, value):
        pass

    @property
    def title(self):
        """ str: The current page title. """
        elements = self.native.xpath("/html/head/title | /html/title")
        return elements[0].text if elements else None

    def synchronize(self, func=None, **kwargs):
        # Simple nodes don't need to wait.
        return func if func else lambda func: func

    def _find_xpath(self, xpath):
        return self.native.xpath(xpath)

    def _find_css(self, css):
        xpath = to_xpath(x.css(css))
        return self._find_xpath(xpath)


def _get_option_value(option):
    return option.get("value") or inner_content(option)
