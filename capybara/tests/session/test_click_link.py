import pytest
import re

from capybara.exceptions import ElementNotFound
from capybara.tests.app import AppError


class TestClickLink:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    @pytest.mark.requires("server")
    def test_raises_any_errors_caught_inside_the_server(self, session):
        session.visit("/error")
        with pytest.raises(AppError):
            session.click_link("foo")

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

    def test_finds_links_with_a_given_href(self, session):
        session.click_link("labore", href="/with_simple_html")
        assert session.has_text("Bar")

    def test_raises_if_link_with_given_href_not_found(self, session):
        with pytest.raises(ElementNotFound):
            session.click_link("labore", href="invalid_href")

    def test_finds_a_link_matching_an_all_matching_regex_pattern(self, session):
        session.click_link("labore", href=re.compile(r".+"))
        assert session.has_text("Bar")

    def test_finds_a_link_matching_an_exact_regex_pattern(self, session):
        session.click_link("labore", href=re.compile(r"\/with_simple_html"))
        assert session.has_text("Bar")

    def test_finds_a_link_matching_a_partial_regex_pattern(self, session):
        session.click_link("labore", href=re.compile(r"\/with_simple"))
        assert session.has_text("Bar")

    def test_raises_an_error_if_no_link_href_matched_the_pattern(self, session):
        with pytest.raises(ElementNotFound):
            session.click_link("labore", href=re.compile(r"invalid_pattern"))
        with pytest.raises(ElementNotFound):
            session.click_link("labore", href=re.compile(r".+d+"))

    def test_follows_relative_links(self, session):
        session.visit("/")
        session.click_link("Relative")
        assert session.has_text("This is a test")

    def test_follows_protocol_relative_links(self, session):
        session.click_link("Protocol")
        assert session.has_text("Another World")

    def test_follows_redirects(self, session):
        session.click_link("Redirect")
        assert session.has_text("You landed")

    def test_follows_redirects_back_to_itself(self, session):
        session.click_link("BackToMyself")
        assert session.has_css("#referrer", text=re.compile(r"/with_html$"))
        assert session.has_text("This is a test")

    def test_adds_query_string_to_current_url_with_naked_query_string(self, session):
        session.click_link("Naked Query String")
        assert session.has_text("Query String sent")

    def test_does_nothing_on_anchor_links(self, session):
        session.fill_in("test_field", value="blah")
        session.click_link("Normal Anchor")
        assert session.find_field("test_field").value == "blah"
        session.click_link("Blank Anchor")
        assert session.find_field("test_field").value == "blah"
        session.click_link("Blank JS Anchor")
        assert session.find_field("test_field").value == "blah"

    def test_does_nothing_on_url_and_anchor_links_for_the_same_page(self, session):
        session.fill_in("test_field", value="blah")
        session.click_link("Anchor on same page")
        assert session.find_field("test_field").value == "blah"

    def test_follows_link_on_url_and_anchor_links_for_a_different_page(self, session):
        session.click_link("Anchor on different page")
        assert session.has_text("Bar")

    def test_raises_an_error_for_links_with_no_href(self, session):
        with pytest.raises(ElementNotFound):
            session.click_link("No Href")

    def test_follows_links_by_partial_match_when_exact_is_false(self, session):
        session.click_link("abo", exact=False)
        assert session.has_text("Bar")

    def test_raises_an_error_for_partial_match_when_exact_is_true(self, session):
        with pytest.raises(ElementNotFound):
            session.click_link("abo", exact=True)

    def test_uses_options_without_locator(self, session):
        session.click_link(href="/foo")
        assert session.has_content("Another World")
