from capybara.driver.node import Node as Base
from capybara.helpers import normalize_text


class Node(Base):
    @property
    def tag_name(self):
        return self.native.tag_name

    @property
    def value(self):
        return self.native.get_attribute("value")

    @property
    def text(self):
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

    def set(self, value):
        tag_name = self.tag_name
        type_attr = self["type"]

        if tag_name == "input" and type_attr == "checkbox":
            current = self.native.get_attribute("checked") == "true"

            if current ^ value:
                self.click()

    @property
    def checked(self):
        return self.native.is_selected()
