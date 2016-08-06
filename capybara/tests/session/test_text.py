class TestText:
    def test_returns_the_text_of_the_page(self, session):
        session.visit("/with_simple_html")
        assert session.text == "Bar"

    def test_ignores_invisible_text(self, session):
        session.visit("/with_html")
        assert session.find("xpath", "//*[@id='hidden-text']").text == "Some of this text is"
