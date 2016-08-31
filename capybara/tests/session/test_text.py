class TestText:
    def test_returns_the_text_of_the_page(self, session):
        session.visit("/with_simple_html")
        assert session.text == "Bar"

    def test_ignores_invisible_text(self, session):
        session.visit("/with_html")
        assert session.find("xpath", "//*[@id='hidden-text']").text == "Some of this text is"

    def test_strips_whitespace(self, session):
        session.visit("/with_html")
        assert "text with whitespace" in session.find("xpath", "//*[@id='second']").text


class TestAllText:
    def test_shows_invisible_text(self, session):
        session.visit("/with_html")
        assert session.find("id", "hidden-text").all_text == "Some of this text is hidden!"


class TestVisibleText:
    def test_ignores_invisible_text(self, session):
        session.visit("/with_html")
        assert session.find("id", "hidden-text").visible_text == "Some of this text is"
