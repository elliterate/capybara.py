from lxml import etree
import re

from capybara.utils import inner_content


class HTML(object):
    def __init__(self, source):
        if not source:
            source = "<html/>"

        parser = etree.HTMLParser(encoding="utf-8")
        tree = etree.HTML(source, parser=parser)

        for element in tree.xpath("//textarea"):
            content = inner_content(element)
            content = re.sub("\A\n", "", content)
            for child in element.getchildren():
                element.remove(child)
            element.text = content

        self.tree = tree

    def xpath(self, xpath):
        return self.tree.xpath(xpath)
