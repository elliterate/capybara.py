import atexit
from selenium import webdriver

from capybara.driver.base import Base
from capybara.selenium.node import Node
from capybara.utils import cached_property


class Driver(Base):
    def __init__(self, app):
        self.app = app

    @cached_property
    def browser(self):
        browser = webdriver.Firefox()
        atexit.register(browser.quit)
        return browser

    @property
    def title(self):
        return self.browser.title

    @property
    def html(self):
        return self.browser.page_source

    @property
    def text(self):
        return self.browser.text

    def visit(self, url):
        self.browser.get(url)

    def _find_xpath(self, xpath):
        return [Node(self, element) for element in self.browser.find_elements_by_xpath(xpath)]
