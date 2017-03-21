from xpath import dsl as x
from xpath.renderer import to_xpath

from capybara.driver.base import Base
from capybara.werkzeug.browser import Browser
from capybara.werkzeug.node import Node


class Driver(Base):
    redirect_limit = 5

    def __init__(self, app):
        self.app = app
        self._browser = None

    @property
    def browser(self):
        if self._browser is None:
            self._browser = Browser(self)
        return self._browser

    @property
    def current_url(self):
        return self.browser.current_url

    @property
    def title(self):
        elements = self.browser.dom.xpath("/html/head/title")
        return elements[0].text if len(elements) else None

    @property
    def html(self):
        return self.browser.html

    def visit(self, path):
        self.browser.visit(path)

    def follow(self, method, path, params=None):
        self.browser.follow(method, path, params)

    def submit(self, method, path, params):
        self.browser.submit(method, path, params)

    def reset(self):
        self._browser = None

    def _find_css(self, css):
        elements = self.browser.dom.xpath(to_xpath(x.css(css)))
        return [Node(self, element) for element in elements]

    def _find_xpath(self, xpath):
        elements = self.browser.dom.xpath(xpath)
        return [Node(self, element) for element in elements]
