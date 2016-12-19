# coding=utf-8
from __future__ import unicode_literals

import capybara


class TestText:
    def test_returns_the_text_of_the_page(self, session):
        session.visit("/with_simple_html")
        assert session.text == "Bar"

    def test_ignores_invisible_text_by_default(self, session):
        session.visit("/with_html")
        assert session.find("xpath", "//*[@id='hidden-text']").text == "Some of this text is"

    def test_ignores_invisible_text_if_ignore_hidden_elements_is_true(self, session):
        session.visit("/with_html")
        assert session.find("id", "hidden-text").text == "Some of this text is"
        capybara.ignore_hidden_elements = False
        assert session.find("id", "hidden-text").text == "Some of this text is hidden!"

    def test_ignores_invisible_text_if_visible_text_only_is_true(self, session):
        session.visit("/with_html")
        capybara.visible_text_only = True
        assert session.find("id", "hidden-text").text == "Some of this text is"
        capybara.ignore_hidden_elements = False
        assert session.find("id", "hidden-text").text == "Some of this text is"

    def test_ignores_invisible_text_if_ancestor_is_invisible(self, session):
        session.visit("/with_html")
        assert session.find("id", "hidden_via_ancestor", visible=False).text == ""

    def test_strips_whitespace(self, session):
        session.visit("/with_html")
        assert "text with whitespace" in session.find("xpath", "//*[@id='second']").text

    def test_returns_unicode_text(self, session):
        session.visit("/with_html")
        assert session.find("id", "unicode-text").text == "이름"


class TestAllText:
    def test_shows_invisible_text(self, session):
        session.visit("/with_html")
        assert session.find("id", "hidden-text").all_text == "Some of this text is hidden!"


class TestVisibleText:
    def test_ignores_invisible_text(self, session):
        session.visit("/with_html")
        assert session.find("id", "hidden-text").visible_text == "Some of this text is"
