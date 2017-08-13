import json
from lxml import etree
from werkzeug.datastructures import ImmutableMultiDict


def extract_results(session):
    session.assert_selector("//pre[@id='results']")

    tree = etree.HTML(session.body)
    element = tree.xpath("//pre[@id='results']")[0]

    def inner_html(elem):
        return "".join(
            [elem.text or ""] +
            [etree.tostring(child).decode("utf-8") for child in elem] +
            [elem.tail or ""])

    return ImmutableMultiDict(json.loads(inner_html(element)))


def ismarionette(session):
    return getattr(session.driver, "_marionette", False)


def isselenium(session):
    try:
        from capybara.selenium.driver import Driver
    except ImportError:
        # If we can't import it, then it can't be in use.
        return False

    return isinstance(session.driver, Driver)
