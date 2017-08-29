import pytest

from capybara.exceptions import Ambiguous, ElementNotFound
from capybara.selector import add_selector, remove_selector


class TestSibling:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    @pytest.fixture(autouse=True)
    def teardown_selector(self):
        try:
            yield
        finally:
            remove_selector("data_attribute")

    def test_finds_a_prior_sibling_element_using_the_given_locator(self, session):
        el = session.find("css", "#mid_sibling")
        assert el.sibling("//div[@data-pre]")["id"] == "pre_sibling"

    def test_finds_a_following_sibling_element_using_the_given_locator(self, session):
        el = session.find("css", "#mid_sibling")
        assert el.sibling("//div[@data-post]")["id"] == "post_sibling"

    def test_raises_an_error_if_there_are_multiple_matches(self, session):
        el = session.find("css", "#mid_sibling")
        with pytest.raises(Ambiguous):
            el.sibling("//div")

    def test_finds_the_first_element_using_the_given_css_selector(self, session):
        el = session.find("css", "#mid_sibling")
        assert el.sibling("css", "#pre_sibling").has_text("Pre Sibling")
        assert el.sibling("css", "#post_sibling").has_text("Post Sibling")

    def test_uses_a_custom_selector(self, session):
        with add_selector("data_attribute") as s:
            @s.xpath
            def xpath(attr):
                return ".//*[@data-{}]".format(attr)

        el = session.find("css", "#mid_sibling")
        assert el.sibling("data_attribute", "pre").has_text("Pre Sibling")
        assert el.sibling("data_attribute", "post").has_text("Post Sibling")

    def test_raises_element_not_found_with_a_useful_default_message_if_nothing_was_found(self, session):
        el = session.find("css", "#child")
        with pytest.raises(ElementNotFound) as excinfo:
            el.sibling("xpath", "//div[@id='nosuchthing']")
        assert (
            "Unable to find xpath \"//div[@id='nosuchthing']\" that is a sibling of css "
            "'#child'") in str(excinfo)
