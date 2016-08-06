from capybara.driver.node import Node as Base
from capybara.helpers import normalize_text


class Node(Base):
    @property
    def tag_name(self):
        return self.native.tag_name

    @property
    def text(self):
        return normalize_text(self.native.text)

    def __getitem__(self, name):
        return self.native.get_attribute(name)

    def _find_xpath(self, xpath):
        cls = type(self)
        return [cls(self.driver, element) for element in self.native.find_elements_by_xpath(xpath)]
