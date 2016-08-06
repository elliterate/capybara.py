import pytest

from capybara.exceptions import ExpectationNotMet


class TestAssertText:
    def test_is_true_if_the_given_text_is_on_the_page(self, session):
        session.visit("/with_html")
        assert session.assert_text("est") is True
        assert session.assert_text("Lorem") is True
        assert session.assert_text("Redirect") is True
        assert session.assert_text("text with whitespace") is True
        assert session.assert_text("text     with \n\n whitespace") is True

    def test_raises_an_error_if_the_given_text_is_not_on_the_page(self, session):
        session.visit("/with_html")
        with pytest.raises(ExpectationNotMet):
            session.assert_text("thisisnotonthepage")

    def test_waits_for_text_to_appear(self, session):
        session.visit("/with_js")
        session.click_link("Click me")
        assert session.assert_text("Has been clicked") is True
