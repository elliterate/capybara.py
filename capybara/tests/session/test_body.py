class TestBody:
    def test_returns_the_unmodified_page_body(self, session):
        session.visit("/")
        assert session.has_text("Hello world!")
        assert "Hello world!" in session.body
