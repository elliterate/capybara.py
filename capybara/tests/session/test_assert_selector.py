import pytest

from capybara.exceptions import ElementNotFound


class TestAssertSelector:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    def test_does_not_raise_if_the_given_selector_is_on_the_page(self, session):
        session.assert_selector("xpath", "//p")

    def test_raises_if_the_given_selector_is_not_on_the_page(self, session):
        with pytest.raises(ElementNotFound):
            session.assert_selector("xpath", "//abbr")
