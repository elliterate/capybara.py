import pytest
from xpath import html

import capybara


class TestFindFirst:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    def test_finds_the_first_element_using_the_given_locator(self, session):
        assert session.find_first("//h1").text == "This is a test"
        assert session.find_first("//input[@id='test_field']").value == "monkey"

    def test_returns_none_when_nothing_was_found(self, session):
        assert session.find_first("//div[@id='nosuchthing']") is None

    def test_accepts_an_xpath_expression_instance(self, session):
        session.visit("/form")
        xpath = html.fillable_field("First Name")
        assert session.find_first(xpath).value == "John"

    def test_finds_the_first_element_using_the_given_css_selector(self, session):
        assert session.find_first("css", "h1").text == "This is a test"
        assert session.find_first("css", "input[id='test_field']").value == "monkey"

    def test_finds_the_first_element_using_the_given_xpath_query(self, session):
        assert session.find_first("xpath", "//h1").text == "This is a test"
        assert session.find_first("xpath", "//input[@id='test_field']").value == "monkey"

    def test_finds_the_first_element_using_the_given_locator_when_css_is_the_default_selector(self, session):
        capybara.default_selector = "css"
        assert session.find_first("h1").text == "This is a test"
        assert session.find_first("input[id='test_field']").value == "monkey"

    def test_finds_the_first_element_using_the_given_locator_in_a_scope(self, session):
        session.visit("/with_scope")
        with session.scope("xpath", "//div[@id='for_bar']"):
            assert session.find_first(".//form") is not None
