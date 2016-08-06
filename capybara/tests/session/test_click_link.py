import pytest

from capybara.exceptions import ElementNotFound


class TestClickLink:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    def test_follows_links_by_id(self, session):
        session.click_link("foo")
        assert session.has_text("Another World")

    def test_follows_links_by_text(self, session):
        session.click_link("labore")
        assert session.has_text("Bar")

    def test_follows_links_by_partial_text(self, session):
        session.click_link("abo")
        assert session.has_text("Bar")

    def test_follows_links_by_title(self, session):
        session.click_link("awesome title")
        assert session.has_text("Bar")

    def test_follows_links_by_partial_title(self, session):
        session.click_link("some titl")
        assert session.has_text("Bar")

    def test_follows_links_by_alternate_text_of_descendant_image(self, session):
        session.click_link("awesome image")
        assert session.has_text("Bar")

    def test_follows_links_by_partial_alternate_text_of_descendant_image(self, session):
        session.click_link("some imag")
        assert session.has_text("Bar")

    def test_raises_an_error_for_a_locator_that_does_not_exist(self, session):
        with pytest.raises(ElementNotFound):
            session.click_link("does not exist")

    def test_raises_an_error_for_links_with_no_href(self, session):
        with pytest.raises(ElementNotFound):
            session.click_link("No Href")

    def test_follows_links_by_partial_match_when_exact_is_false(self, session):
        session.click_link("abo", exact=False)
        assert session.has_text("Bar")

    def test_raises_an_error_for_partial_match_when_exact_is_true(self, session):
        with pytest.raises(ElementNotFound):
            session.click_link("abo", exact=True)
