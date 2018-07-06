import pytest

import capybara


class TestHasAllOfSelectors:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    def test_is_true_if_the_given_selectors_are_on_the_page(self, session):
        assert session.has_all_of_selectors("css", "p a#foo", "h2#h2one", "h2#h2two") is True

    def test_is_false_if_any_of_the_given_selectors_are_not_on_the_page(self, session):
        assert session.has_all_of_selectors("css", "p #afoo", "h2#h2three", "h2#h2one") is False

    def test_uses_default_selector(self, session):
        capybara.default_selector = "css"
        assert session.has_all_of_selectors("p a#foo", "h2#h2one", "h2#h2two")
        assert not session.has_all_of_selectors("p #afoo", "h2#h2three", "h2#h2one")

    def test_respects_scopes_when_used_with_a_context(self, session):
        with session.scope("//p[@id='first']"):
            assert session.has_all_of_selectors(".//a[@id='foo']")
            assert not session.has_all_of_selectors(".//a[@id='red']")

    def test_respects_scopes_when_called_on_elements(self, session):
        el = session.find("//p[@id='first']")
        assert el.has_all_of_selectors(".//a[@id='foo']")
        assert not el.has_all_of_selectors(".//a[@id='red']")

    def test_applies_options_to_all_locators(self, session):
        assert session.has_all_of_selectors(
            "field", "normal", "additional_newline", field_type="textarea")
        assert not session.has_all_of_selectors(
            "field", "normal", "test_field", "additional_newline", field_type="textarea")

    @pytest.mark.requires("js")
    def test_does_not_raise_error_if_all_the_elements_appear_before_given_wait_duration(self, session):
        with capybara.using_wait_time(0.1):
            session.visit("/with_js")
            session.click_link("Click me")
            assert session.has_all_of_selectors(
                "css", "a#clickable", "a#has-been-clicked", "#drag", wait=5)
