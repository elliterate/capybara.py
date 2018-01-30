import atexit
from contextlib import contextmanager
from selenium.common.exceptions import (
    NoAlertPresentException,
    NoSuchWindowException,
    TimeoutException,
    UnexpectedAlertPresentException,
    WebDriverException)
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep, time

import capybara
from capybara.driver.base import Base
from capybara.exceptions import ExpectationNotMet, ModalNotFound
from capybara.helpers import toregex, desc
from capybara.selenium.browser import get_browser
from capybara.selenium.node import Node
from capybara.utils import cached_property, isregex


class Driver(Base):
    """
    A Capybara driver that uses Selenium WebDriver to drive a real browser.

    Args:
        app (object): The WSGI-compliant app to drive.
        browser (str, optional): The name of the browser to use. Defaults to "firefox".
        desired_capabilities (Dict[str, str | bool], optional): Desired
            capabilities of the underlying browser. Defaults to a set of
            reasonable defaults provided by Selenium.
        options: Arbitrary keyword arguments for the underlying Selenium driver.
    """

    def __init__(self, app, browser="firefox", desired_capabilities=None, **options):
        self.app = app
        self._browser_name = browser
        self._desired_capabilities = desired_capabilities
        self._options = options
        self._frame_handles = []

    @property
    def needs_server(self):
        return True

    @cached_property
    def browser(self):
        capabilities = self._desired_capabilities

        if self._firefox:
            capabilities = (capabilities or DesiredCapabilities.FIREFOX).copy()
            # Auto-accept unload alerts triggered by navigating away.
            if capabilities.get("marionette"):
                capabilities["unhandledPromptBehavior"] = "dismiss"
            else:
                capabilities["unexpectedAlertBehaviour"] = "ignore"

        browser = get_browser(self._browser_name, capabilities=capabilities, **self._options)
        atexit.register(browser.quit)
        return browser

    @property
    def current_url(self):
        return self.browser.current_url

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
        if frame == "top":
            self._frame_handles = []
            self.browser.switch_to.default_content()
        elif frame == "parent":
            self._frame_handles.pop()
            self.browser.switch_to.default_content()
            for frame_handle in self._frame_handles:
                self.browser.switch_to.frame(frame_handle)
        else:
            self._frame_handles.append(frame.native)
            self.browser.switch_to.frame(frame.native)

    @property
    def current_window_handle(self):
        return self.browser.current_window_handle

    def window_size(self, handle):
        with self._window(handle):
            size = self.browser.get_window_size()
            return [size["width"], size["height"]]

    def resize_window_to(self, handle, width, height):
        with self._window(handle):
            self.browser.set_window_size(width, height)

    def maximize_window(self, handle):
        with self._window(handle):
            self.browser.maximize_window()

    def close_window(self, handle):
        with self._window(handle):
            self.browser.close()

    @property
    def window_handles(self):
        return self.browser.window_handles

    def open_new_window(self):
        self.browser.execute_script("window.open();")

    def switch_to_window(self, handle):
        self.browser.switch_to.window(handle)

    @property
    def no_such_window_error(self):
        return NoSuchWindowException

    def visit(self, url):
        self.browser.get(url)

    def go_back(self):
        self.browser.back()

    def go_forward(self):
        self.browser.forward()

    def execute_script(self, script, *args):
        args = [arg.native if isinstance(arg, Node) else arg for arg in args]
        return self.browser.execute_script(script, *args)

    def evaluate_script(self, script, *args):
        result = self.execute_script("return {0}".format(script), *args)
        return self._wrap_element_script_result(result)

    def save_screenshot(self, path, **kwargs):
        self.browser.get_screenshot_as_file(path)

    @contextmanager
    def accept_modal(self, modal_type, text=None, response=None, wait=None):
        yield
        modal = self._find_modal(text=text, wait=wait)
        if response:
            modal.send_keys(response)
        modal.accept()

    @contextmanager
    def dismiss_modal(self, modal_type, text=None, wait=None):
        yield
        modal = self._find_modal(text=text, wait=wait)
        modal.dismiss()

    def reset(self):
        # Avoid starting the browser just to reset the session.
        if "browser" in self.__dict__:
            navigated = False
            start_time = time()
            while True:
                try:
                    # Only trigger a navigation if we haven't done it already,
                    # otherwise it can trigger an endless series of unload modals.
                    if not navigated:
                        self.browser.delete_all_cookies()
                        self.browser.get("about:blank")
                        navigated = True

                    while True:
                        if not len(self._find_xpath("/html/body/*")):
                            break
                        if time() - start_time >= 10:
                            raise ExpectationNotMet("Timed out waiting for Selenium session reset")
                        sleep(0.05)

                    break
                except UnexpectedAlertPresentException:
                    # This error is thrown if an unhandled alert is on the page.
                    try:
                        self.browser.switch_to.alert.accept()

                        # Allow time for the modal to be handled.
                        sleep(0.25)
                    except NoAlertPresentException:
                        # The alert is now gone. Nothing to do.
                        pass

                    # Try cleaning up the browser again.
                    continue

    @property
    def invalid_element_errors(self):
        return (WebDriverException,)

    @property
    def _marionette(self):
        return self._firefox and self.browser.w3c

    @property
    def _firefox(self):
        return self._browser_name in ["ff", "firefox"]

    def _find_css(self, css):
        return [Node(self, element) for element in self.browser.find_elements_by_css_selector(css)]

    def _find_xpath(self, xpath):
        return [Node(self, element) for element in self.browser.find_elements_by_xpath(xpath)]

    def _find_modal(self, text=None, wait=None):
        wait = wait or capybara.default_max_wait_time
        try:
            alert = WebDriverWait(self.browser, wait).until(EC.alert_is_present())
            regexp = toregex(text)
            if not regexp.search(alert.text):
                qualifier = "matching" if isregex(text) else "with"
                raise ModalNotFound("Unable to find modal dialog {0} {1}".format(qualifier, desc(text)))
            return alert
        except TimeoutException:
            raise ModalNotFound("Unable to find modal dialog")

    @contextmanager
    def _window(self, handle):
        original_handle = self.current_window_handle
        if handle == original_handle:
            yield
        else:
            self.switch_to_window(handle)
            try:
                yield
            finally:
                self.switch_to_window(original_handle)

    def _wrap_element_script_result(self, arg):
        if isinstance(arg, list):
            return [self._wrap_element_script_result(e) for e in arg]
        elif isinstance(arg, dict):
            return {k: self._wrap_element_script_result(v) for k, v in iter(arg.items())}
        elif isinstance(arg, WebElement):
            return Node(self, arg)
        else:
            return arg
