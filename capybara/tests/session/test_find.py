import pytest

from capybara.selector import add_selector, remove_selector


class TestFind:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

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
