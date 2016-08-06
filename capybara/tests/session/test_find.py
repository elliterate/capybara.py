import pytest
from xpath import dsl as x

from capybara.exceptions import ElementNotFound
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

    def test_finds_the_first_element_using_the_given_xpath_selector_locator(self, session):
        assert session.find("xpath", "//h1").text == "This is a test"

    def test_uses_a_custom_selector(self, session):
        with add_selector("beatle") as s:
            s.xpath = lambda name: ".//*[@id='{}']".format(name)

        assert session.find("beatle", "john").text == "John"
        assert session.find("beatle", "paul").text == "Paul"


class TestFindExact(FindTestCase):
    def test_matches_exactly_when_true(self, session):
        xpath_expr = x.descendant("input")[x.attr("id").is_("test_field")]
        assert session.find("xpath", xpath_expr, exact=True)["value"] == "monkey"

        with pytest.raises(ElementNotFound):
            xpath_expr = x.descendant("input")[x.attr("id").is_("est_fiel")]
            session.find("xpath", xpath_expr, exact=True)

    def test_matches_loosely_when_false(self, session):
        xpath_expr = x.descendant("input")[x.attr("id").is_("test_field")]
        assert session.find("xpath", xpath_expr, exact=False)["value"] == "monkey"

        xpath_expr = x.descendant("input")[x.attr("id").is_("est_fiel")]
        assert session.find("xpath", xpath_expr, exact=False)["value"] == "monkey"
