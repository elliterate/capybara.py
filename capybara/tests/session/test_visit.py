class TestVisit:
    def test_fetches_a_response_from_the_driver_with_a_relative_url(self, session):
        session.visit("/")
        assert session.has_text("Hello world!")
        session.visit("/foo")
        assert session.has_text("Another World")
