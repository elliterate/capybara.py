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


def isfirefox(session):
    """ bool: Whether the session is using Firefox. """
    return getattr(session.driver, "_firefox", False)


def ismarionette(session):
    """ bool: Whether the session is using Marionette. """
    return getattr(session.driver, "_marionette", False)


def ismarionettelt(version, session):
    """
    Whether the session is using Marionette with Firefox less than the given version.

    Args:
        version (int): The Firefox version to test.
        session (Session): The Capybara session.

    Returns:
        bool: Whether the session is using Marionette with Firefox less than the given version.
    """

    return ismarionette(session) and int(session.driver.browser.capabilities['browserVersion'].split(".")[0]) < version


def isselenium(session):
    """ bool: Whether the session is using Selenium. """
    try:
        from capybara.selenium.driver import Driver
    except ImportError:
        # If we can't import it, then it can't be in use.
        return False

    return isinstance(session.driver, Driver)
