import re
from werkzeug.test import Client, create_environ
from werkzeug.wrappers import BaseResponse, Request

import capybara
from capybara.compat import ParseResult, urlparse
from capybara.html import HTML
from capybara.utils import cached_property, decode_bytes


class Browser(object):
    def __init__(self, driver):
        self.driver = driver
        self.last_request = None
        self.last_response = None
        self._current_scheme = "http"
        self._current_netloc = None
        self._dom = None

    @property
    def app(self):
        return self.driver.app

    @cached_property
    def client(self):
        return Client(self.app, BaseResponse)

    @property
    def current_url(self):
        if self.last_request:
            return self.last_request.url

    def visit(self, path):
        self._reset_host()
        self._process_and_follow_redirects("GET", path)

    def follow(self, method, path, params=None):
        if (
            # 1. Anchor on the current page
            re.sub(r"^{}".format(re.escape(self._request_path)), "", path).startswith("#") or
            # 2. Inline JavaScript
            path.lower().startswith("javascript:")
        ):
            return

        self._process_and_follow_redirects(method, path, params, {"Referer": self.current_url})

    def submit(self, method, path, params):
        if not path:
            path = self._request_path

        self._process_and_follow_redirects(method, path, params, {"Referer": self.current_url})

    @property
    def html(self):
        return decode_bytes(self.last_response.data) if self.last_response else ""

    @property
    def dom(self):
        if self._dom is None:
            self._dom = HTML(self.html)
        return self._dom

    @property
    def _request_path(self):
        return self.last_request.path if self.last_request else "/"

    def _process_and_follow_redirects(self, method, path, params=None, headers=None):
        self._process(method, path, params, headers)
        for _ in range(self.driver.redirect_limit):
            if 300 <= self.last_response.status_code < 400:
                path = self.last_response.headers["Location"]
                self._process("GET", path, headers=headers)

    def _process(self, method, path, params=None, headers=None):
        self._dom = None

        requested_uri = urlparse(path)

        base_uri = ParseResult(
            scheme=requested_uri.scheme or self._current_scheme,
            netloc=requested_uri.netloc or self._current_netloc,
            path="",
            params="",
            query="",
            fragment="")

        requested_path = (
            self._request_path if path.startswith("?")
            else requested_uri.path)

        path_uri = ParseResult(
            scheme="",
            netloc="",
            path=requested_path,
            params=requested_uri.params,
            query=requested_uri.query,
            fragment="")

        self._current_scheme = base_uri.scheme
        self._current_netloc = base_uri.netloc

        env = create_environ(method=method,
                             path=path_uri.geturl(),
                             base_url=base_uri.geturl() or None,
                             data=params,
                             headers=headers)

        self.last_request = Request(env)
        self.last_response = self.client.open(env)

    def _reset_host(self):
        if capybara.app_host:
            uri = urlparse(capybara.app_host)
            self._current_scheme = uri.scheme
            self._current_netloc = uri.netloc
