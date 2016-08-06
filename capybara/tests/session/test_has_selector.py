import pytest

import capybara


class TestHasSelector:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    def test_is_true_if_the_given_selector_is_on_the_page(self, session):
        assert session.has_selector("xpath", "//p")
        assert session.has_selector("css", "p a#foo")
        assert session.has_selector("//p[contains(.,'est')]")

    def test_is_false_if_the_given_selector_is_not_on_the_page(self, session):
        assert not session.has_selector("xpath", "//abbr")
        assert not session.has_selector("css", "p a#doesnotexist")
        assert not session.has_selector("//p[contains(.,'thisstringisnotonpage')]")

    def test_uses_default_selector(self, session):
        capybara.default_selector = "css"
        assert not session.has_selector("p a#doesnotexist")
        assert session.has_selector("p a#foo")

    def test_respects_scopes(self, session):
        with session.scope("//p[@id='first']"):
            assert session.has_selector(".//a[@id='foo']")
            assert not session.has_selector(".//a[@id='red']")
