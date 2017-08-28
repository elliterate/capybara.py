import pytest

from capybara.exceptions import Ambiguous, ElementNotFound
from capybara.selector import add_selector, remove_selector


class TestAncestor:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    @pytest.fixture(autouse=True)
    def teardown_selector(self):
        try:
            yield
        finally:
            remove_selector("level")

    def test_finds_the_ancestor_element_using_the_given_locator(self, session):
        el = session.find("css", "#first_image")
        assert el.ancestor("//p").has_text("Lorem ipsum dolor")
        assert el.ancestor("//a")["aria-label"] == "Go to simple"

    def test_finds_the_ancestor_element_using_the_given_locator_and_options(self, session):
        el = session.find("css", "#child")
        assert el.ancestor("//div", text="Ancestor Ancestor Ancestor")["id"] == "ancestor3"

    def test_raises_an_error_if_there_are_multiple_matches(self, session):
        el = session.find("css", "#child")
        with pytest.raises(Ambiguous):
            el.ancestor("//div")
        with pytest.raises(Ambiguous):
            el.ancestor("//div", text="Ancestor")

    def test_finds_the_first_element_using_the_given_ccss_selector(self, session):
        el = session.find("css", "#first_image")
        assert el.ancestor("css", "p").has_text("Lorem ipsum dolor")
        assert el.ancestor("css", "a")["aria-label"] == "Go to simple"

    def test_supports_pseudo_selectors(self, session):
        el = session.find("css", "#button_img")
        assert el.ancestor("css", "button:disabled")["id"] == "ancestor_button"

    def test_finds_the_first_element_using_the_given_xpath_query(self, session):
        el = session.find("css", "#first_image")
        assert el.ancestor("xpath", "//p").has_text("Lorem ipsum dolor")
        assert el.ancestor("xpath", "//a")["aria-label"] == "Go to simple"

    def test_uses_a_custom_selector(self, session):
        with add_selector("level") as s:
            @s.xpath
            def xpath(num):
                return ".//*[@id='ancestor{num}']".format(num=num)

        el = session.find("css", "#child")
        assert el.ancestor("level", 1).text == "Ancestor Child"
        assert el.ancestor("level", 3).text == "Ancestor Ancestor Ancestor Child"

    def test_raises_element_not_found_with_a_useful_default_message_if_nothing_was_found(self, session):
        el = session.find("css", "#child")
        with pytest.raises(ElementNotFound) as excinfo:
            el.ancestor("xpath", "//div[@id='nosuchthing']")
        assert (
            "Unable to find xpath \"//div[@id='nosuchthing']\" that is an ancestor of css "
            "'#child'") in str(excinfo)

    def test_limits_the_ancestors_to_inside_the_scope(self, session):
        with session.scope("css", "#ancestor2"):
            el = session.find("css", "#child")
            assert el.ancestor("css", "div", text="Ancestor")["id"] == "ancestor1"
