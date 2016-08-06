import pytest

import capybara
from capybara.exceptions import ElementNotFound


class TestAssertSelector:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    def test_does_not_raise_if_the_given_selector_is_on_the_page(self, session):
        session.assert_selector("xpath", "//p")
        session.assert_selector("css", "p a#foo")
        session.assert_selector("//p[contains(.,'est')]")

    def test_raises_if_the_given_selector_is_not_on_the_page(self, session):
        with pytest.raises(ElementNotFound):
            session.assert_selector("xpath", "//abbr")
        with pytest.raises(ElementNotFound):
            session.assert_selector("css", "p a#doesnotexist")
        with pytest.raises(ElementNotFound):
            session.assert_selector("//p[contains(.,'thisstringisnotonpage')]")

    def test_uses_default_selector(self, session):
        capybara.default_selector = "css"
        with pytest.raises(ElementNotFound):
            session.assert_selector("p a#doesnotexist")
        session.assert_selector("p a#foo")

    def test_respects_scopes(self, session):
        with session.scope("//p[@id='first']"):
            session.assert_selector(".//a[@id='foo']")
            with pytest.raises(ElementNotFound):
                session.assert_selector(".//a[@id='red']")
