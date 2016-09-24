from selenium.webdriver.common.action_chains import ActionChains

from capybara.exceptions import ReadOnlyElementError, UnselectNotAllowed
from capybara.driver.node import Node as Base
from capybara.helpers import normalize_text


class Node(Base):
    @property
    def tag_name(self):
        return self.native.tag_name

    @property
    def visible(self):
        return self.native.is_displayed()

    @property
    def value(self):
        if self.tag_name == "select" and self.multiple:
            options = self.native.find_elements_by_xpath(".//option")
            selected_options = filter(lambda opt: opt.is_selected(), options)
            return [opt.get_attribute("value") for opt in selected_options]
        else:
            return self.native.get_attribute("value")

    @property
    def selected(self):
        return self.native.is_selected()

    @property
    def multiple(self):
        val = self["multiple"]
        return bool(val) and val != "false"

    @property
    def path(self):
        path = [self] + list(reversed(self._find_xpath("ancestor::*")))

        result = []
        while path:
            node = path.pop(0)
            parent = path[0] if path else None

            if parent:
                siblings = parent._find_xpath(node.tag_name)
                if len(siblings) == 1:
                    result.insert(0, node.tag_name)
                else:
                    index = siblings.index(node)
                    result.insert(0, "{tag}[{i}]".format(tag=node.tag_name, i=index + 1))
            else:
                result.insert(0, node.tag_name)

        return "/" + "/".join(result)

    @property
    def all_text(self):
        text = self.driver.browser.execute_script("return arguments[0].textContent", self.native)
        return normalize_text(text)

    @property
    def visible_text(self):
        return normalize_text(self.native.text)

    def __getitem__(self, name):
        return self.native.get_attribute(name)

    def _find_css(self, css):
        cls = type(self)
        return [cls(self.driver, element) for element in self.native.find_elements_by_css_selector(css)]

    def _find_xpath(self, xpath):
        cls = type(self)
        return [cls(self.driver, element) for element in self.native.find_elements_by_xpath(xpath)]

    def click(self):
        self.native.click()

    def double_click(self):
        ActionChains(self.driver.browser).double_click(self.native).perform()

    def drag_to(self, element):
        ActionChains(self.driver.browser).drag_and_drop(self.native, element.native).perform()

    def hover(self):
        ActionChains(self.driver.browser).move_to_element(self.native).perform()

    def right_click(self):
        ActionChains(self.driver.browser).context_click(self.native).perform()

    def select_option(self):
        if not self.selected:
            self.native.click()

    def send_keys(self, *args):
        self.native.send_keys(*args)

    def set(self, value):
        tag_name = self.tag_name
        type_attr = self["type"]

        if tag_name == "input" and type_attr == "radio":
            self.click()
        elif tag_name == "input" and type_attr == "checkbox":
            current = self.native.get_attribute("checked") == "true"

            if current ^ value:
                self.click()
        elif tag_name == "textarea" or tag_name == "input":
            if self.readonly:
                raise ReadOnlyElementError()

            # Clear field by JavaScript assignment of the value property.
            self.driver.browser.execute_script("arguments[0].value = ''", self.native)
            self.native.send_keys(value)
        elif self["isContentEditable"]:
            self.native.click()
            script = """
                var range = document.createRange();
                range.selectNodeContents(arguments[0]);
                window.getSelection().addRange(range);
            """
            self.driver.browser.execute_script(script, self.native)
            self.native.send_keys(value)

    def unselect_option(self):
        if not self._select_node.multiple:
            raise UnselectNotAllowed("Cannot unselect option from single select box.")

        if self.selected:
            self.native.click()

    def __eq__(self, other):
        return self.native == other.native

    def __hash__(self):
        return hash(self.native)

    @property
    def checked(self):
        return self.selected

    @property
    def selected(self):
        return self.native.is_selected()

    @property
    def disabled(self):
        return not self.native.is_enabled()

    @property
    def readonly(self):
        val = self["readonly"]
        return bool(val) and val != "false"

    @property
    def _select_node(self):
        return self._find_xpath("./ancestor::select")[0]
