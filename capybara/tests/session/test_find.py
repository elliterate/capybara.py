import pytest
from xpath import dsl as x

from capybara.exceptions import Ambiguous, ElementNotFound
from capybara.selector import add_selector, remove_selector


class FindTestCase:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")


class TestFind(FindTestCase):
    @pytest.fixture(autouse=True)
    def teardown_selector(self):
        try:
            yield
        finally:
            remove_selector("beatle")

    def test_finds_the_first_element_using_the_given_locator(self, session):
        assert session.find("//h1").text == "This is a test"
        assert session.find("//input[@id='test_field']").value == "monkey"

    def test_raises_an_error_if_there_are_multiple_matches(self, session):
        with pytest.raises(Ambiguous):
            session.find("//a")

    def test_waits_for_asynchronous_load(self, session):
        session.visit("/with_js")
        session.click_link("Click me")
        assert "Has been clicked" in session.find("css", "a#has-been-clicked").text

    def test_finds_the_first_element_with_using_the_given_css_selector_locator(self, session):
        assert session.find("css", "h1").text == "This is a test"
        assert session.find("css", "input[id='test_field']").value == "monkey"

    def test_supports_css_pseudo_selectors(self, session):
        assert session.find("css", "input:disabled").value == "This is disabled"

    def test_finds_the_first_element_using_the_given_xpath_selector_locator(self, session):
        assert session.find("xpath", "//h1").text == "This is a test"
        assert session.find("xpath", "//input[@id='test_field']").value == "monkey"

    def test_uses_a_custom_selector(self, session):
        with add_selector("beatle") as s:
            s.xpath = lambda name: ".//*[@id='{}']".format(name)

        assert session.find("beatle", "john").text == "John"
        assert session.find("beatle", "paul").text == "Paul"

    def test_finds_an_element_using_the_given_locator_in_a_scope(self, session):
        session.visit("/with_scope")
        with session.scope("xpath", "//div[@id='for_bar']"):
            assert "With Simple HTML" in session.find(".//li[1]").text

    def test_supports_pseudo_selectors_in_a_scope(self, session):
        session.visit("/with_scope")
        with session.scope("xpath", "//div[@id='for_bar']"):
            assert session.find("css", "input:disabled").value == "James"


class TestFindExact(FindTestCase):
    def test_matches_exactly_when_true(self, session):
        xpath_expr = x.descendant("input")[x.attr("id").is_("test_field")]
        assert session.find("xpath", xpath_expr, exact=True).value == "monkey"

        with pytest.raises(ElementNotFound):
            xpath_expr = x.descendant("input")[x.attr("id").is_("est_fiel")]
            session.find("xpath", xpath_expr, exact=True)

    def test_matches_loosely_when_false(self, session):
        xpath_expr = x.descendant("input")[x.attr("id").is_("test_field")]
        assert session.find("xpath", xpath_expr, exact=False).value == "monkey"

        xpath_expr = x.descendant("input")[x.attr("id").is_("est_fiel")]
        assert session.find("xpath", xpath_expr, exact=False).value == "monkey"
