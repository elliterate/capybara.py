class TestTitle:
    def test_returns_the_title_of_the_page(self, session):
        session.visit("/with_title")
        assert session.title == "Test Title"
