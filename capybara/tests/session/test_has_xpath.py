import pytest

import capybara


class TestHasXPath:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    def test_is_true_if_the_given_selector_is_on_the_page(self, session):
        assert session.has_xpath("//p")
        assert session.has_xpath("//p//a[@id='foo']")
        assert session.has_xpath("//p[contains(.,'est')]")

    def test_is_false_if_the_given_selector_is_not_on_the_page(self, session):
        assert not session.has_xpath("//abbr")
        assert not session.has_xpath("//p//a[@id='doesnotexist']")
        assert not session.has_xpath("//p[contains(.,'thisstringisnotonpage')]")

    def test_uses_xpath_even_if_default_selector_is_css(self, session):
        capybara.default_selector = "css"
        assert not session.has_xpath("//p//a[@id='doesnotexist']")

    def test_respects_scopes(self, session):
        with session.scope("//p[@id='first']"):
            assert session.has_xpath(".//a[@id='foo']")
            assert not session.has_xpath(".//a[@id='red']")

    def test_waits_for_content_to_appear(self, session):
        session.visit("/with_js")
        session.click_link("Click me")
        assert session.has_xpath("//input[@type='submit' and @value='New Here']")
