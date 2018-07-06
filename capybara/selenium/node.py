from contextlib import contextmanager
from functools import wraps
from selenium.common.exceptions import MoveTargetOutOfBoundsException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

try:
    from selenium.common.exceptions import ElementClickInterceptedException
except ImportError:
    class ElementClickInterceptedException(WebDriverException):
        pass

from capybara.exceptions import ReadOnlyElementError, UnselectNotAllowed
from capybara.driver.node import Node as Base
from capybara.helpers import normalize_whitespace


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
        return normalize_whitespace(text)

    @property
    def visible_text(self):
        return normalize_whitespace(self.native.text)

    def __getitem__(self, name):
        return self.native.get_attribute(name)

    def _find_css(self, css):
        cls = type(self)
        return [cls(self.driver, element)
                for element in self.native.find_elements_by_css_selector(css)]

    def _find_xpath(self, xpath):
        cls = type(self)
        return [cls(self.driver, element)
                for element in self.native.find_elements_by_xpath(xpath)]

    def click(self, *keys, **offset):
        try:
            if not any(keys) and not self._has_coords(offset):
                self.native.click()
            else:
                @self._scroll_if_needed
                def click():
                    with self._action_with_modifiers(keys, offset) as a:
                        a.click() if self._has_coords(offset) else a.click(self.native)
                click()

        except WebDriverException as e:
            if (
                # Marionette
                isinstance(e, ElementClickInterceptedException) or

                # Chrome
                "Other element would receive the click" in e.msg
            ):
                self._scroll_to_center()

            raise

    def double_click(self, *keys, **offset):
        @self._scroll_if_needed
        def double_click():
            with self._action_with_modifiers(keys, offset) as a:
                a.double_click() if self._has_coords(offset) else a.double_click(self.native)
        double_click()

    def drag_to(self, element):
        ActionChains(self.driver.browser).drag_and_drop(self.native, element.native).perform()

    def hover(self):
        ActionChains(self.driver.browser).move_to_element(self.native).perform()

    def right_click(self, *keys, **offset):
        @self._scroll_if_needed
        def right_click():
            with self._action_with_modifiers(keys, offset) as a:
                a.context_click() if self._has_coords(offset) else a.context_click(self.native)
        right_click()

    def select_option(self):
        if not self.selected and not self.disabled:
            self.native.click()

    def send_keys(self, *args):
        self.native.send_keys(*args)

    def set(self, value, clear=None):
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

            if clear == "backspace":
                # Clear field by sending the correct number of backspace keys.
                backspaces = [Keys.BACKSPACE] * len(self.value)
                self.native.send_keys(*(backspaces + [value]))
            else:
                # Clear field by JavaScript assignment of the value property.
                self.driver.browser.execute_script("arguments[0].value = ''", self.native)
                self.native.send_keys(value)
        elif self["isContentEditable"]:
            self.native.click()
            script = """
                var range = document.createRange();
                var sel = window.getSelection();
                range.selectNodeContents(arguments[0]);
                sel.removeAllRanges();
                sel.addRange(range);
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

    @staticmethod
    def _has_coords(options):
        return bool(options.get('x')) and bool(options.get('y'))

    def _scroll_if_needed(self, fn):
        @wraps(fn)
        def wrapper():
            try:
                fn()
            except MoveTargetOutOfBoundsException:
                self._scroll_to_center()
                fn()

        return wrapper

    def _scroll_to_center(self):
        try:
            self.driver.execute_script("""
                arguments[0].scrollIntoView({behavior: 'instant', block: 'center', inline: 'center'})
            """, self)
        except:
            # Swallow error if scrollIntoView with options isn't supported.
            pass

    @contextmanager
    def _action_with_modifiers(self, keys, offset):
        actions = ActionChains(self.driver.browser)
        if self._has_coords(offset):
            actions.move_to_element_with_offset(self.native, offset['x'], offset['y'])
        self._modifiers_down(actions, keys)
        yield actions
        self._modifiers_up(actions, keys)
        actions.perform()

    @staticmethod
    def _modifiers_down(actions, keys):
        for key in keys:
            actions.key_down(key)

    @staticmethod
    def _modifiers_up(actions, keys):
        for key in keys:
            actions.key_up(key)
