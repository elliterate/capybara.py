# coding=utf-8
from __future__ import unicode_literals

import pytest
import re

import capybara
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

    def test_is_true_if_the_given_unicode_text_is_on_the_page(self, session):
        session.visit("/with_html")
        assert session.assert_text("이름") is True

    def test_raises_an_error_if_the_given_unicode_text_is_not_on_the_page(self, session):
        session.visit("/with_html")
        with pytest.raises(ExpectationNotMet):
            session.assert_text("论坛")

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

    def test_is_true_if_the_text_in_the_page_matches_given_regex(self, session):
        session.visit("/with_html")
        assert session.assert_text(re.compile(r"Lorem")) is True

    def test_raises_error_if_the_text_in_the_page_does_not_match_given_regex(self, session):
        session.visit("/with_html")
        with pytest.raises(ExpectationNotMet) as excinfo:
            session.assert_text(re.compile(r"xxxxyzzz"))
        assert "expected to find text matching 'xxxxyzzz' in 'This is a test Header Class" in str(excinfo.value)

    def test_excapes_any_characters_that_would_have_special_meaning_in_a_regex(self, session):
        session.visit("/with_html")
        with pytest.raises(ExpectationNotMet):
            session.assert_text(".orem")

    @pytest.mark.requires("js")
    def test_waits_for_text_to_appear(self, session):
        session.visit("/with_js")
        session.click_link("Click me")
        assert session.assert_text("Has been clicked") is True

    def test_is_true_if_the_text_occurs_within_the_range_given(self, session):
        session.visit("/with_count")
        assert session.assert_text("count", between=range(1, 4)) is True

    def test_is_false_if_the_text_occurs_more_or_fewer_times_than_range(self, session):
        session.visit("/with_count")
        with pytest.raises(ExpectationNotMet) as excinfo:
            session.assert_text("count", between=range(0, 2))
        assert "expected to find text 'count' between 0 and 1 times but found 2 times" in str(excinfo.value)

    @pytest.mark.requires("js")
    def test_finds_element_if_it_appears_before_given_wait_duration(self, session):
        with capybara.using_wait_time(0):
            session.visit("/with_js")
            session.find("css", "#reload-list").click()
            session.find("css", "#the-list").assert_text("Foo Bar", wait=0.9)

    @pytest.mark.requires("js")
    def test_raises_error_if_it_appears_after_given_wait_duration(self, session):
        with capybara.using_wait_time(0):
            session.visit("/with_js")
            session.find("css", "#reload-list").click()
            el = session.find("css", "#the-list", visible=False)
            with pytest.raises(ExpectationNotMet):
                el.assert_text("all", "Foo Bar", wait=0.3)


class TestAssertTextCount:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    def test_ignores_other_filters_when_count_is_specified(self, session):
        session.assert_text("Header", count=5, minimum=6, maximum=0, between=range(0, 5))

    def test_fails_if_minimum_is_not_met(self, session):
        with pytest.raises(ExpectationNotMet):
            session.assert_text("Header", minimum=0, maximum=0, between=range(2, 8))

    def test_fails_if_maximum_is_not_met(self, session):
        with pytest.raises(ExpectationNotMet):
            session.assert_text("Header", minimum=0, maximum=0, between=range(2, 8))

    def test_fails_if_between_is_not_met(self, session):
        with pytest.raises(ExpectationNotMet):
            session.assert_text("Header", minimum=0, maximum=5, between=range(0, 5))

    def test_succeeds_if_all_combined_expectations_are_met(self, session):
        session.assert_text("Header", minimum=0, maximum=5, between=range(2, 8))


class TestAssertNoText:
    def test_raises_error_if_the_given_text_is_on_the_page_at_least_once(self, session):
        session.visit("/with_html")
        with pytest.raises(ExpectationNotMet) as excinfo:
            session.assert_no_text("Lorem")
        assert "expected not to find text 'Lorem' in 'This is a test Header Class" in str(excinfo.value)

    def test_is_true_if_scoped_to_an_element_which_does_not_have_the_text(self, session):
        session.visit("/with_html")
        with session.scope("//a[@title='awesome title']"):
            assert session.assert_no_text("monkey") is True

    def test_is_true_if_given_text_is_on_the_page_but_not_visible(self, session):
        session.visit("/with_html")
        assert session.assert_no_text("Inside element with hidden selector") is True

    def test_raises_error_if_all_given_and_text_is_invisible(self, session):
        session.visit("/with_html")
        el = session.find("css", "#hidden-text", visible=False)
        with pytest.raises(ExpectationNotMet) as excinfo:
            el.assert_no_text("all", "Some of this text is hidden!")
        assert "expected not to find text 'Some of this text is hidden!' in 'Some of this text is hidden!'" in str(excinfo.value)

    def test_raises_error_if_visible_given_and_text_is_visible(self, session):
        session.visit("/with_html")
        el = session.find("css", "#some-hidden-text", visible=False)
        with pytest.raises(ExpectationNotMet) as excinfo:
            el.assert_no_text("visible", "hidden")
        assert "expected not to find text 'hidden' in 'Some of this text is not hidden'" in str(excinfo.value)

    def test_is_true_if_the_text_in_the_page_does_not_match_given_regex(self, session):
        session.visit("/with_html")
        session.assert_no_text(re.compile(r"xxxxyzzz"))

    def test_is_true_if_the_text_does_not_occur_the_given_number_of_times(self, session):
        session.visit("/with_count")
        assert session.assert_no_text("count", count=3) is True

    def test_raises_if_the_text_occurs_the_given_number_of_times(self, session):
        session.visit("/with_count")
        with pytest.raises(ExpectationNotMet) as excinfo:
            session.assert_no_text("count", count=2)
        assert "expected not to find text 'count' 2 times" in str(excinfo.value)

    @pytest.mark.requires("js")
    def test_does_not_find_text_if_it_appears_after_given_wait_duration(self, session):
        session.visit("/with_js")
        session.click_link("Click me")
        session.find("css", "#reload-list").click()
        session.find("css", "#the-list").assert_no_text("Foo Bar", wait=0.3)
