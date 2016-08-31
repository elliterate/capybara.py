import pytest
from xpath import html

import capybara


class FindFirstTestCase:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")


class TestFindFirst(FindFirstTestCase):
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


class TestFindFirstVisible(FindFirstTestCase):
    def test_only_finds_visible_nodes_when_true(self, session):
        assert session.find_first("css", "a#invisible", visible=True) is None
        assert session.find_first("css", "a#visible", visible=True) is not None

    def test_finds_nodes_regardless_of_whether_they_are_invisible_when_false(self, session):
        assert session.find_first("css", "a#invisible", visible=False) is not None
        assert session.find_first("css", "a#visible", visible=False) is not None

    def test_finds_nodes_regardless_of_whether_they_are_invisible_when_all(self, session):
        assert session.find_first("css", "a#invisible", visible="all") is not None
        assert session.find_first("css", "a#visible", visible="all") is not None

    def test_finds_only_hidden_nodes_when_hidden(self, session):
        assert session.find_first("css", "a#invisible", visible="hidden") is not None
        assert session.find_first("css", "a#visible", visible="hidden") is None

    def test_finds_only_visible_nodes_when_visible(self, session):
        assert session.find_first("css", "a#invisible", visible="visible") is None
        assert session.find_first("css", "a#visible", visible="visible") is not None
