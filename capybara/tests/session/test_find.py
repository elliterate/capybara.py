import pytest
import time
from xpath import dsl as x

import capybara
from capybara.exceptions import Ambiguous, ElementNotFound, FrozenInTime
from capybara.selector import add_selector, remove_selector
from capybara.tests.compat import patch


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

    @pytest.mark.requires("js")
    def test_waits_for_asynchronous_load(self, session):
        session.visit("/with_js")
        session.click_link("Click me")
        assert "Has been clicked" in session.find("css", "a#has-been-clicked").text

    def test_casts_text_argument_to_string(self, session):
        assert session.find("css", ".number", text=42).has_text("42")

    @pytest.mark.requires("js")
    def test_does_not_wait_for_asynchronous_load_when_false_given(self, session):
        session.visit("/with_js")
        session.click_link("Click me")
        with pytest.raises(ElementNotFound):
            session.find("css", "a#has-been-clicked", wait=False)

    @pytest.mark.requires("js")
    def test_does_not_find_element_if_it_appears_after_given_wait_duration(self, session):
        session.visit("/with_js")
        session.click_link("Slowly")
        with pytest.raises(ElementNotFound):
            session.find("css", "a#slow-clicked", wait=0.2)

    @pytest.mark.requires("js")
    def test_finds_element_if_it_appears_before_given_wait_duration(self, session):
        session.visit("/with_js")
        session.click_link("Click me")
        assert "Has been clicked" in session.find("css", "a#has-been-clicked", wait=0.9).text

    def test_raises_an_error_suggesting_that_capybara_is_stuck_in_time(self, session):
        session.visit("/with_js")
        now = time.time()

        import capybara.node.base
        with patch.object(capybara.node.base, "time", return_value=now):
            with pytest.raises(FrozenInTime):
                session.find("//isnotthere")

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

    def test_supports_a_custom_filter(self, session):
        assert session.find("css", "input", filter=lambda node: node.disabled)["name"] == "disabled_text"


class TestFindMatch(FindTestCase):
    def test_defaults_to_capybara_match(self, session):
        capybara.match = "one"
        with pytest.raises(Ambiguous):
            session.find("css", ".multiple")

        capybara.match = "first"
        assert session.find("css", ".multiple").text == "multiple one"

    def test_raises_an_error_when_unknown_option_given(self, session):
        with pytest.raises(Exception):
            session.find("css", ".singular", match="schmoo")


class TestFindMatchOne(FindTestCase):
    def test_raises_an_error_when_multiple_matches_exist(self, session):
        with pytest.raises(Ambiguous):
            session.find("css", ".multiple", match="one")

    def test_raises_an_error_even_if_one_match_is_exact_and_the_others_are_inexact(self, session):
        xpath_expr = x.descendant()[x.attr("class").is_("almost_singular")]
        with pytest.raises(Ambiguous):
            session.find("xpath", xpath_expr, exact=False, match="one")

    def test_returns_the_element_if_there_is_only_one(self, session):
        assert session.find("css", ".singular", match="one").text == "singular"

    def test_raises_an_error_if_there_is_no_match(self, session):
        with pytest.raises(ElementNotFound):
            session.find("css", ".does-not-exist", match="one")


class TestFindMatchFirst(FindTestCase):
    def test_returns_the_first_matched_element(self, session):
        assert session.find("css", ".multiple", match="first").text == "multiple one"

    def test_raises_an_error_if_there_is_no_match(self, session):
        with pytest.raises(ElementNotFound):
            session.find("css", ".does-not-exist", match="first")


class TestFindMatchSmartAndInexact(FindTestCase):
    def test_raises_an_error_when_there_are_multiple_exact_matches(self, session):
        xpath_expr = x.descendant()[x.attr("class").is_("multiple")]
        with pytest.raises(Ambiguous):
            session.find("xpath", xpath_expr, match="smart", exact=False)

    def test_finds_a_single_exact_match_when_there_also_are_inexact_matches(self, session):
        xpath_expr = x.descendant()[x.attr("class").is_("almost_singular")]
        result = session.find("xpath", xpath_expr, match="smart", exact=False)
        assert result.text == "almost singular"

    def test_raises_an_error_when_there_are_multiple_inexact_matches(self, session):
        xpath_expr = x.descendant()[x.attr("class").is_("almost_singul")]
        with pytest.raises(Ambiguous):
            session.find("xpath", xpath_expr, match="smart", exact=False)

    def test_finds_a_single_inexact_match(self, session):
        xpath_expr = x.descendant()[x.attr("class").is_("almost_singular but")]
        result = session.find("xpath", xpath_expr, match="smart", exact=False)
        assert result.text == "almost singular but not quite"

    def test_raises_an_error_if_there_is_no_match(self, session):
        with pytest.raises(ElementNotFound):
            session.find("css", ".does-not-exist", match="smart", exact=False)


class TestFindMatchSmartAndExact(FindTestCase):
    def test_raises_an_error_when_there_are_multiple_exact_matches(self, session):
        xpath_expr = x.descendant()[x.attr("class").is_("multiple")]
        with pytest.raises(Ambiguous):
            session.find("xpath", xpath_expr, match="smart", exact=True)

    def test_finds_a_single_exact_match_when_there_also_are_inexact_matches(self, session):
        xpath_expr = x.descendant()[x.attr("class").is_("almost_singular")]
        result = session.find("xpath", xpath_expr, match="smart", exact=True)
        assert result.text == "almost singular"

    def test_raises_an_error_when_there_are_multiple_inexact_matches(self, session):
        xpath_expr = x.descendant()[x.attr("class").is_("almost_singul")]
        with pytest.raises(ElementNotFound):
            session.find("xpath", xpath_expr, match="smart", exact=True)

    def test_raises_an_error_when_there_is_a_single_inexact_matches(self, session):
        xpath_expr = x.descendant()[x.attr("class").is_("almost_singular but")]
        with pytest.raises(ElementNotFound):
            session.find("xpath", xpath_expr, match="smart", exact=True)

    def test_raises_an_error_if_there_is_no_match(self, session):
        with pytest.raises(ElementNotFound):
            session.find("css", ".does-not-exist", match="smart", exact=True)


class TestFindMatchPreferExactAndInexact(FindTestCase):
    def test_picks_the_first_one_when_there_are_multiple_exact_matches(self, session):
        xpath_expr = x.descendant()[x.attr("class").is_("multiple")]
        result = session.find("xpath", xpath_expr, match="prefer_exact", exact=False)
        assert result.text == "multiple one"

    def test_finds_a_single_exact_match_when_there_also_are_inexact_matches(self, session):
        xpath_expr = x.descendant()[x.attr("class").is_("almost_singular")]
        result = session.find("xpath", xpath_expr, match="prefer_exact", exact=False)
        assert result.text == "almost singular"

    def test_picks_the_first_one_when_there_are_multiple_inexact_matches(self, session):
        xpath_expr = x.descendant()[x.attr("class").is_("almost_singul")]
        result = session.find("xpath", xpath_expr, match="prefer_exact", exact=False)
        assert result.text == "almost singular but not quite"

    def test_finds_a_single_inexact_match(self, session):
        xpath_expr = x.descendant()[x.attr("class").is_("almost_singular but")]
        result = session.find("xpath", xpath_expr, match="prefer_exact", exact=False)
        assert result.text == "almost singular but not quite"

    def test_raises_an_error_if_there_is_no_match(self, session):
        with pytest.raises(ElementNotFound):
            session.find("css", ".does-not-exist", match="prefer_exact", exact=False)


class TestFindMatchPreferExactAndExact(FindTestCase):
    def test_picks_the_first_one_when_there_are_multiple_exact_matches(self, session):
        xpath_expr = x.descendant()[x.attr("class").is_("multiple")]
        result = session.find("xpath", xpath_expr, match="prefer_exact", exact=True)
        assert result.text == "multiple one"

    def test_finds_a_single_exact_match_when_there_also_are_inexact_matches(self, session):
        xpath_expr = x.descendant()[x.attr("class").is_("almost_singular")]
        result = session.find("xpath", xpath_expr, match="prefer_exact", exact=True)
        assert result.text == "almost singular"

    def test_raises_an_error_if_there_are_multiple_inexact_matches(self, session):
        xpath_expr = x.descendant()[x.attr("class").is_("almost_singul")]
        with pytest.raises(ElementNotFound):
            session.find("xpath", xpath_expr, match="prefer_exact", exact=True)

    def test_raises_an_error_if_there_is_a_single_inexact_match(self, session):
        xpath_expr = x.descendant()[x.attr("class").is_("almost_singular but")]
        with pytest.raises(ElementNotFound):
            session.find("xpath", xpath_expr, match="prefer_exact", exact=True)

    def test_raises_an_error_if_there_is_no_match(self, session):
        with pytest.raises(ElementNotFound):
            session.find("css", ".does-not-exist", match="prefer_exact", exact=True)


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

    def test_defaults_to_capybara_exact(self, session):
        xpath_expr = x.descendant("input")[x.attr("id").is_("est_fiel")]

        capybara.exact = True
        with pytest.raises(ElementNotFound):
            session.find("xpath", xpath_expr)

        capybara.exact = False
        session.find("xpath", xpath_expr)
