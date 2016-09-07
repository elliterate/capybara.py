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

    def test_takes_scopes_into_account(self, session):
        session.visit("/with_html")
        with session.scope("//a[@title='awesome title']"):
            assert session.assert_text("labore") is True

    def test_raises_if_scoped_to_an_element_which_does_not_have_the_text(self, session):
        session.visit("/with_html")
        with session.scope("//a[@title='awesome title']"):
            with pytest.raises(ExpectationNotMet) as excinfo:
                session.assert_text("monkey")
        assert "expected to find text 'monkey' in 'labore'" in str(excinfo.value)

    def test_is_true_if_all_given_and_text_is_invisible(self, session):
        session.visit("/with_html")
        assert session.assert_text("all", "Some of this text is hidden!") is True

    def test_raises_an_error_with_a_helpful_message_if_the_requested_text_is_present_but_invisible(self, session):
        session.visit("/with_html")
        el = session.find("css", "#hidden-text")
        with pytest.raises(ExpectationNotMet) as excinfo:
            el.assert_text("visible", "Some of this text is hidden!")
        assert "it was found 1 time including non-visible text" in str(excinfo.value)

    def test_raises_error_with_a_helpful_message_if_the_requested_text_is_present_but_with_incorrect_case(self, session):
        session.visit("/with_html")
        with pytest.raises(ExpectationNotMet) as excinfo:
            session.assert_text("Text With Whitespace")
        assert "it was found 1 time using a case insensitive search" in str(excinfo.value)

    def test_waits_for_text_to_appear(self, session):
        session.visit("/with_js")
        session.click_link("Click me")
        assert session.assert_text("Has been clicked") is True
