import pytest

from capybara.exceptions import ElementNotFound
from capybara.tests.helpers import extract_results


class TestClickLinkOrButton:
    def test_clicks_on_a_link(self, session):
        session.visit("/with_html")
        session.click_link_or_button("labore")
        assert session.has_text("Bar")

    def test_clicks_on_a_button(self, session):
        session.visit("/form")
        session.click_link_or_button("awe123")
        assert extract_results(session)["form[first_name]"] == "John"

    def test_clicks_on_a_button_with_no_type_attribute(self, session):
        session.visit("/form")
        session.click_link_or_button("no_type")
        assert extract_results(session)["form[first_name]"] == "John"

    def test_aliased_as_click_on(self, session):
        session.visit("/form")
        session.click_on("awe123")
        assert extract_results(session)["form[first_name]"] == "John"

    @pytest.mark.requires("js")
    def test_waits_for_asynchronous_load(self, session):
        session.visit("/with_js")
        session.click_link("Click me")
        session.click_link_or_button("Has been clicked")

    def test_raises_an_error_with_a_locator_that_does_not_exist(self, session):
        session.visit("/with_html")
        with pytest.raises(ElementNotFound):
            session.click_link_or_button("does not exist")

    def test_clicks_on_approximately_matching_link(self, session):
        session.visit("/with_html")
        session.click_link_or_button("abore")
        assert session.has_text("Bar")

    def test_clicks_on_approximately_matching_button(self, session):
        session.visit("/form")
        session.click_link_or_button("awe")
        assert extract_results(session)["form[first_name]"] == "John"

    def test_clicks_on_links_which_incorrectly_have_the_disabled_attribute(self, session):
        session.visit("/with_html")
        session.click_link_or_button("Disabled link")
        assert session.has_text("Bar")


class TextExactClickLinkOrButton:
    def test_does_not_click_on_approximately_matching_link(self, session):
        session.visit("/with_html")
        with pytest.raises(ElementNotFound):
            session.click_link_or_button("abore", exact=True)

    def test_does_not_click_on_approximately_matching_button(self, session):
        session.visit("/form")
        with pytest.raises(ElementNotFound):
            session.click_link_or_button("awe", exact=True)
