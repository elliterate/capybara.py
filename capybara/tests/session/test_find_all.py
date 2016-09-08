import pytest
from xpath import html

import capybara
from capybara.exceptions import ExpectationNotMet


class FindAllTestCase:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")


class TestFindAll(FindAllTestCase):
    def test_finds_all_elements_using_the_given_locator(self, session):
        assert len(session.find_all("//p")) == 3
        assert session.find_all("//h1")[0].text == "This is a test"
        assert session.find_all("//input[@id='test_field']")[0].value == "monkey"

    def test_returns_an_empty_result_when_nothing_was_found(self, session):
        assert len(session.find_all("//div[@id='nosuchthing']")) == 0

    def test_accepts_an_xpath_expression_instance(self, session):
        session.visit("/form")
        xpath = html.fillable_field("Name")
        result = [r.value for r in session.find_all(xpath)]
        assert "Smith" in result
        assert "John" in result
        assert "John Smith" in result

    def test_finds_all_elements_using_the_given_css_selector(self, session):
        assert session.find_all("css", "h1")[0].text == "This is a test"
        assert session.find_all("css", "input[id='test_field']")[0].value == "monkey"

    def test_finds_all_elements_when_given_a_list_of_css_selectors(self, session):
        assert len(session.find_all("css", "h1, p")) == 4

    def test_finds_all_elements_using_the_given_xpath_query(self, session):
        assert session.find_all("xpath", "//h1")[0].text == "This is a test"
        assert session.find_all("xpath", "//input[@id='test_field']")[0].value == "monkey"

    def test_finds_the_first_element_using_the_given_locator_when_css_is_the_default_selector(self, session):
        capybara.default_selector = "css"
        assert session.find_all("h1")[0].text == "This is a test"
        assert session.find_all("input[id='test_field']")[0].value == "monkey"

    def test_finds_any_element_using_the_given_locator_in_a_scope(self, session):
        session.visit("/with_scope")
        with session.scope("xpath", "//div[@id='for_bar']"):
            assert len(session.find_all(".//li")) == 2


class TestFindAllVisible(FindAllTestCase):
    def test_only_finds_visible_nodes_when_true(self, session):
        assert len(session.find_all("css", "a.simple", visible=True)) == 1

    def test_finds_nodes_regardless_of_whether_they_are_invisible_when_false(self, session):
        assert len(session.find_all("css", "a.simple", visible=False)) == 2

    def test_defaults_to_capybara_ignore_hidden_elements(self, session):
        capybara.ignore_hidden_elements = True
        assert len(session.find_all("css", "a.simple")) == 1
        capybara.ignore_hidden_elements = False
        assert len(session.find_all("css", "a.simple")) == 2


class TestFindAllCount(FindAllTestCase):
    def test_succeeds_when_the_number_of_elements_found_matches_the_expectation(self, session):
        session.find_all("css", "h1, p", count=4)

    def test_raises_when_the_number_of_elements_found_does_not_match_the_expectation(self, session):
        with pytest.raises(ExpectationNotMet):
            session.find_all("css", "h1, p", count=5)


class TestFindAllMinimum(FindAllTestCase):
    def test_succeeds_when_the_number_of_elements_found_matches_the_expectation(self, session):
        session.find_all("css", "h1, p", minimum=0)

    def test_raises_when_the_number_of_elements_found_does_not_match_the_expectation(self, session):
        with pytest.raises(ExpectationNotMet):
            session.find_all("css", "h1, p", minimum=5)


class TestFindAllMaximum(FindAllTestCase):
    def test_succeeds_when_the_number_of_elements_found_matches_the_expectation(self, session):
        session.find_all("css", "h1, p", maximum=4)

    def test_raises_when_the_number_of_elements_found_does_not_match_the_expectation(self, session):
        with pytest.raises(ExpectationNotMet):
            session.find_all("css", "h1, p", maximum=0)


class TestFindAllBetween(FindAllTestCase):
    def test_succeeds_when_the_number_of_elements_found_matches_the_expectation(self, session):
        session.find_all("css", "h1, p", between=range(2, 7))

    def test_raises_when_the_number_of_elements_found_does_not_match_the_expectation(self, session):
        with pytest.raises(ExpectationNotMet):
            session.find_all("css", "h1, p", between=range(0, 3))
