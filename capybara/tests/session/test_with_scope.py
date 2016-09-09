import pytest

from capybara.exceptions import ElementNotFound
from capybara.tests.helpers import extract_results


class TestScope:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_scope")

    def test_asserts_content_in_the_given_scope(self, session):
        with session.scope("css", "#for_foo"):
            assert not session.has_text("First Name")
        assert session.has_text("First Name")

    def test_accepts_additional_options(self, session):
        with session.scope("css", "#for_bar li", text="With Simple HTML"):
            session.click_link("Go")
        assert session.has_text("Bar")

    def test_clicks_links_in_the_given_xpath_scope(self, session):
        with session.scope("xpath", "//div[@id='for_bar']//li[contains(.,'With Simple HTML')]"):
            session.click_link("Go")
        assert session.has_text("Bar")

    def test_clicks_links_in_the_given_node(self, session):
        node_of_interest = session.find("css", "#for_bar li", text="With Simple HTML")
        with session.scope(node_of_interest):
            session.click_link("Go")
        assert session.has_text("Bar")

    def test_respects_the_inner_scope_of_nested_scopes(self, session):
        with session.scope("//div[@id='for_bar']"):
            with session.scope(".//li[contains(.,'Bar')]"):
                session.click_link("Go")
        assert session.has_text("Another World")

    def test_respects_the_outer_scope_of_nested_scopes(self, session):
        with session.scope("//div[@id='another_foo']"):
            with session.scope(".//li[contains(.,'With Simple HTML')]"):
                session.click_link("Go")
        assert session.has_text("Hello world")

    def test_raises_an_error_if_the_scope_is_not_found_on_the_page(self, session):
        with pytest.raises(ElementNotFound):
            with session.scope("//div[@id='doesnotexist']"):
                pass

    def test_restores_the_scope_when_an_error_is_raised(self, session):
        assert session.has_xpath(".//div[@id='another_foo']")
        with session.scope("//div[@id='for_bar']"):
            assert not session.has_xpath(".//div[@id='another_foo']")
            with pytest.raises(ElementNotFound):
                with session.scope(".//div[@id='doesnotexist']"):
                    pass
            assert not session.has_xpath(".//div[@id='another_foo']")
        assert session.has_xpath(".//div[@id='another_foo']")

    def test_fills_in_a_field_and_clicks_a_button(self, session):
        with session.scope("//li[contains(.,'Bar')]"):
            session.click_button("Go")
        assert extract_results(session)["form[first_name]"] == "Peter"

        session.visit("/with_scope")
        with session.scope("//li[contains(.,'Bar')]"):
            session.fill_in("First Name", value="Dagobert")
            session.click_button("Go")
        assert extract_results(session)["form[first_name]"] == "Dagobert"
