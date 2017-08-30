import pytest
import re

import capybara
from capybara.exceptions import ElementNotFound


class TestFindLink:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    def test_finds_any_field(self, session):
        assert session.find_link("foo").text == "ullamco"
        assert re.compile(r"/with_simple_html$").search(session.find_link("labore")["href"])

    def test_raises_an_error_if_the_field_does_not_exist(self, session):
        with pytest.raises(ElementNotFound):
            session.find_link("Does not exist")

    def test_finds_links_by_partial_match_when_exact_is_false(self, session):
        assert session.find_link("abo", exact=False).text == "labore"

    def test_raises_an_error_for_partial_match_when_exact_is_true(self, session):
        with pytest.raises(ElementNotFound):
            session.find_link("abo", exact=True)

    def test_finds_by_aria_label_attribute_when_enable_aria_label_is_true(self, session):
        capybara.enable_aria_label = True
        assert session.find_link("Go to simple")["href"].endswith("/with_simple_html")

    def test_does_not_find_by_aria_label_attribute_when_enable_aria_label_is_false(self, session):
        capybara.enable_aria_label = False
        with pytest.raises(ElementNotFound):
            session.find_link("Go to simple")

    def test_uses_options_without_locator(self, session):
        assert session.find_link(href="#anchor").text == "Normal Anchor"
