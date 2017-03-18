from io import BytesIO
import os
import re
from werkzeug.datastructures import FileStorage, MultiDict
from xpath import dsl as x
from xpath.renderer import to_xpath

from capybara.werkzeug.node import Node


class Form(Node):
    def params(self, button):
        params = MultiDict()

        types = ["input", "select", "textarea"]
        xpath = x.descendant(*types)[~x.attr("form")]
        if self.native.get("id"):
            xpath += x.anywhere(*types)[x.attr("form") == self.native.get("id")]
        xpath = xpath[~x.attr("disabled")]

        for field in self._find_xpath(to_xpath(xpath)):
            if field.tag_name == "input":
                if field["type"] in ["checkbox", "radio"]:
                    if field.checked:
                        params.add(field["name"], field.value)
                elif field["type"] == "file":
                    if self._multipart:
                        if field.value:
                            params.add(
                                field["name"],
                                FileStorage(
                                    stream=open(field.value, "rb"),
                                    filename=os.path.basename(field.value)))
                        else:
                            params.add(
                                field["name"],
                                FileStorage(
                                    stream=BytesIO(),
                                    content_type="application/octet-stream"))
                    else:
                        if field.value:
                            params.add(field["name"], os.path.basename(field.value))
                elif field["type"] in ["submit", "reset", "image"]:
                    pass
                else:
                    params.add(field["name"], field.value)
            elif field.tag_name == "textarea":
                if field.value:
                    params.add(field["name"], re.sub("\n", "\r\n", field.value))
            elif field.tag_name == "select":
                if field["multiple"] == "multiple":
                    options = field.native.xpath(".//option[@selected='selected']")
                    for option in options:
                        params.add(field["name"], option.get("value", option.text))
                else:
                    options = field.native.xpath(".//option[@selected='selected']")
                    if not len(options):
                        options = field.native.xpath(".//option")
                    if len(options):
                        params.add(field["name"], options[0].get("value", options[0].text))

        params.add(button["name"], button["value"] or "")

        return params

    def submit(self, button):
        action = self.native.get("action")
        method = self._request_method
        self.driver.submit(method, action, self.params(button))

    @property
    def _request_method(self):
        if self["method"] and re.compile(r"post", re.IGNORECASE).search(self["method"]):
            return "POST"
        else:
            return "GET"

    @property
    def _multipart(self):
        return self["enctype"] == "multipart/form-data"
