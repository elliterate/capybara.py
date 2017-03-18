from itertools import chain
from xpath import dsl as x
from xpath.renderer import to_xpath

from capybara.driver.node import Node as Base
from capybara.exceptions import ReadOnlyElementError, UnselectNotAllowed
from capybara.helpers import normalize_whitespace
from capybara.node.simple import Simple
from capybara.utils import inner_text


class Node(Base):
    @property
    def tag_name(self):
        return self.native.tag

    def __getitem__(self, name):
        return self._string_node[name]

    def __eq__(self, other):
        return self.native == other.native

    def __hash__(self):
        return hash(self.native)

    @property
    def all_text(self):
        return normalize_whitespace(inner_text(self.native))

    @property
    def visible_text(self):
        return normalize_whitespace(self.unnormalized_text())

    def unnormalized_text(self, check_ancestor_visibility=True):
        if not self._string_node._visible(check_ancestor_visibility):
            return ""
        else:
            parts = (
                [self.native.text] +
                list(chain(*(
                    [Node(self.driver, c).unnormalized_text(check_ancestor_visibility=False),
                     c.tail]
                    for c in self.native.getchildren()))))
            return "".join(filter(None, parts))

    @property
    def disabled(self):
        if self.tag_name in ["option", "optgroup"]:
            return self._string_node.disabled or self._find_xpath("parent::*")[0].disabled
        else:
            return self._string_node.disabled

    @property
    def readonly(self):
        return self._string_node.readonly

    @property
    def multiple(self):
        return self._string_node.multiple

    @property
    def path(self):
        return self._string_node.path

    @property
    def checked(self):
        return self._string_node.checked

    @property
    def selected(self):
        return self._string_node.selected

    @property
    def visible(self):
        return self._string_node.visible

    @property
    def value(self):
        return self._string_node.value

    def click(self):
        if self.tag_name == "a" and self["href"]:
            self.driver.follow("GET", self["href"])
        elif (self.tag_name == "input" and self["type"] in ["submit", "image"]) or \
                (self.tag_name == "button"):
            associated_form = self._form
            if associated_form is not None:
                from capybara.werkzeug.form import Form
                Form(self.driver, associated_form).submit(self)
        elif self.tag_name == "input" and self["type"] in ["checkbox", "radio"]:
            self.set(not self.checked)
        elif self.tag_name == "label":
            labeled_controls = (
                self._find_xpath("//input[@id='{}']".format(self["for"])) if self["for"]
                else self._find_xpath(".//input"))
            labeled_control = labeled_controls[0] if len(labeled_controls) else None

            if labeled_control and (labeled_control._is_checkbox or labeled_control._is_radio):
                labeled_control.set(not labeled_control.checked)

    def set(self, value):
        if self.readonly:
            raise ReadOnlyElementError

        if self._is_radio:
            self._set_radio(value)
        elif self._is_checkbox:
            self._set_checkbox(value)
        elif self._is_input_field:
            self._set_input(value)
        elif self._is_textarea:
            self._set_textarea(value)

    def select_option(self):
        if self.disabled:
            return

        select = self.native.xpath("ancestor::select")[0]

        if select.get("multiple", None) != "multiple":
            options = select.xpath(".//option[@selected='selected']")
            for option in options:
                option.attrib.pop("selected", None)

        self.native.set("selected", "selected")

    def unselect_option(self):
        select = self.native.xpath("ancestor::select")[0]
        if select.get("multiple", None) != "multiple":
            raise UnselectNotAllowed()

        self.native.attrib.pop("selected", None)

    @property
    def _is_input_field(self):
        return self.tag_name == "input"

    @property
    def _is_checkbox(self):
        return self._is_input_field and self["type"] == "checkbox"

    @property
    def _is_radio(self):
        return self._is_input_field and self["type"] == "radio"

    @property
    def _is_textarea(self):
        return self.tag_name == "textarea"

    @property
    def _string_node(self):
        return Simple(self.native)

    @property
    def _form(self):
        elements = (
            self.native.xpath("//form[@id='{}']".format(self["form"])) if self["form"]
            else self.native.xpath(".//ancestor::form"))

        return elements[0] if elements else None

    def _find_css(self, css):
        return self._find_xpath(to_xpath(x.css(css)))

    def _find_xpath(self, xpath):
        cls = type(self)
        elements = self.native.xpath(xpath)
        return [cls(self.driver, element) for element in elements]

    def _set_radio(self, value):
        other_radios = self.native.xpath(to_xpath(
            x.anywhere("input")[x.attr("name") == self["name"]]))
        for node in other_radios:
            node.attrib.pop("checked", None)

        self.native.set("checked", "checked")

    def _set_checkbox(self, value):
        if value:
            self.native.set("checked", "checked")
        else:
            self.native.attrib.pop("checked", None)

    def _set_input(self, value):
        if self["maxlength"]:
            maxlength = int(self["maxlength"])
            value = value[0:maxlength]

        self.native.set("value", value)

    def _set_textarea(self, value):
        for child in self.native.getchildren():
            self.native.remove(child)

        self.native.text = value
