import atexit
from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from capybara.driver.base import Base
from capybara.exceptions import ModalNotFound
from capybara.selenium.node import Node
from capybara.utils import cached_property


class Driver(Base):
    def __init__(self, app):
        self.app = app
        self._frame_handles = []

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

    def switch_to_frame(self, frame):
        if frame == "parent":
            self._frame_handles.pop()
            self.browser.switch_to.default_content()
            for frame_handle in self._frame_handles:
                self.browser.switch_to.frame(frame_handle)
        else:
            self._frame_handles.append(frame.native)
            self.browser.switch_to.frame(frame.native)

    def visit(self, url):
        self.browser.get(url)

    @contextmanager
    def accept_modal(self, modal_type, text=None, wait=None):
        yield
        modal = self._find_modal(text=text, wait=wait)
        modal.accept()


    def _find_css(self, css):
        return [Node(self, element) for element in self.browser.find_elements_by_css_selector(css)]

    def _find_xpath(self, xpath):
        return [Node(self, element) for element in self.browser.find_elements_by_xpath(xpath)]

    def _find_modal(self, text=None, wait=None):
        wait = wait or capybara.default_max_wait_time
        WebDriverWait(self.browser, wait).until(EC.alert_is_present())
        alert = self.browser.switch_to.alert
        if alert is None:
            raise ModalNotFound("Unable to find modal dialog")
        if text and text not in alert.text:
            raise ModalNotFound("Unable to find modal dialog with {0}".format(text))
        return alert
