from capybara.driver.node import Node as Base


class Node(Base):
    @property
    def tag_name(self):
        return self.native.tag_name

    @property
    def text(self):
        return self.native.text

    def _find_xpath(self, xpath):
        cls = type(self)
        return [cls(self.driver, element) for element in self.native.find_elements_by_xpath(xpath)]
