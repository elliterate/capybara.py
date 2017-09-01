# coding=utf-8
from __future__ import unicode_literals

import pytest
import re

import capybara


class TestHasText:
    def test_is_true_if_the_given_text_is_on_the_page_at_least_once(self, session):
        session.visit("/with_html")
        assert session.has_text("est")
        assert session.has_text("Lorem")
        assert session.has_text("Redirect")

    def test_ignores_tags(self, session):
        session.visit("/with_html")
        assert not session.has_text("""exercitation <a href="/foo">ullamco</a> laboris""")
        assert session.has_text("exercitation ullamco laboris")

    def test_ignores_extra_whitespace_and_newlines(self, session):
        session.visit("/with_html")
        assert session.has_text("text with whitespace")

    def test_ignores_white_space_and_newlines_in_the_search_string(self, session):
        session.visit("/with_html")
        assert session.has_text("text     with \n\n whitespace")

    def test_is_false_if_the_given_text_is_not_on_the_page(self, session):
        session.visit("/with_html")
        assert not session.has_text("xxxxyzzz")
        assert not session.has_text("monkey")

    def test_is_true_if_the_given_unicode_text_is_on_the_page(self, session):
        session.visit("/with_html")
        assert session.has_text("이름")

    def test_is_false_if_the_given_unicode_text_is_not_on_the_page(self, session):
        session.visit("/with_html")
        assert not session.has_text("论坛")

    def test_handles_single_quotes_in_the_text(self, session):
        session.visit("/with-quotes")
        assert session.has_text("can't")

    def test_handles_double_quotes_in_the_text(self, session):
        session.visit("/with-quotes")
        assert session.has_text("\"No,\" he said")

    def test_handles_mixed_single_and_double_quotes_in_the_text(self, session):
        session.visit("/with-quotes")
        assert session.has_text("\"you can't do that.\"")

    def test_is_false_if_text_is_in_the_title_tag_in_the_head(self, session):
        session.visit("/with_js")
        assert not session.has_text("with_js")

    def test_is_false_if_text_is_inside_a_script_tag_in_the_body(self, session):
        session.visit("/with_js")
        assert not session.has_text("a javascript comment")
        assert not session.has_text("aVar")

    def test_is_false_if_the_given_text_is_on_the_page_but_not_visible(self, session):
        session.visit("/with_html")
        assert not session.has_text("Inside element with hidden ancestor")

    def test_is_true_if_all_given_and_text_is_invisible(self, session):
        session.visit("/with_html")
        assert session.has_text("all", "Some of this text is hidden!")

    def test_is_true_if_capybara_ignore_hidden_elements_is_false_and_text_is_invisible(self, session):
        capybara.ignore_hidden_elements = False
        session.visit("/with_html")
        assert session.has_text("Some of this text is hidden!")

    def test_is_true_if_the_text_in_the_page_matches_given_regex(self, session):
        session.visit("/with_html")
        assert session.has_text(re.compile(r"Lorem"))

    def test_is_false_if_the_text_in_the_page_does_not_match_given_regex(self, session):
        session.visit("/with_html")
        assert not session.has_text(re.compile(r"xxxxyzzz"))

    def test_is_true_if_text_matches_exact_text_exactly(self, session):
        session.visit("/with_html")
        assert session.find("id", "h2one").has_text("Header Class Test One", exact_text=True)

    def test_is_false_if_text_does_not_match_exact_text_exactly(self, session):
        session.visit("/with_html")
        assert not session.find("id", "h2one").has_text("Header Class Test On", exact_text=True)

    def test_escapes_any_characters_that_would_have_special_meaning_in_a_regex(self, session):
        session.visit("/with_html")
        assert not session.has_text(".orem")

    def test_accepts_non_string_parameters(self, session):
        session.visit("/with_html")
        assert session.has_text(42)

    def test_is_true_when_passed_none(self, session):
        session.visit("/with_html")
        assert session.has_text(None)

    @pytest.mark.requires("js")
    def test_waits_for_text_to_appear(self, session):
        session.visit("/with_js")
        session.click_link("Click me")
        assert session.has_text("Has been clicked")

    def test_is_true_if_the_text_occurs_within_the_range_given(self, session):
        session.visit("/with_count")
        assert session.has_text("count", between=range(1, 4))
        assert session.has_text(re.compile(r"count"), between=range(2, 3))

    def test_is_false_if_the_text_occurs_more_or_fewer_times_than_range(self, session):
        session.visit("/with_count")
        assert not session.has_text("count", between=range(0, 2))
        assert not session.has_text("count", between=range(3, 11))
        assert not session.has_text(re.compile(r"count"), between=range(2, 2))

    def test_is_true_if_the_text_occurs_the_given_number_of_times(self, session):
        session.visit("/with_count")
        assert session.has_text("count", count=2)

    def test_is_false_if_the_text_occurs_a_different_number_of_times_than_given(self, session):
        session.visit("/with_count")
        assert not session.has_text("count", count=0)
        assert not session.has_text("count", count=1)
        assert not session.has_text(re.compile(r"count"), count=3)

    def test_coerces_count_to_an_integer(self, session):
        session.visit("/with_count")
        assert session.has_text("count", count="2")
        assert not session.has_text("count", count="3")

    def test_is_true_when_text_occurs_same_or_fewer_times_than_given(self, session):
        session.visit("/with_count")
        assert session.has_text("count", maximum=2)
        assert session.has_text("count", maximum=3)

    def test_is_false_when_text_occurs_more_times_than_given(self, session):
        session.visit("/with_count")
        assert not session.has_text("count", maximum=1)
        assert not session.has_text(re.compile(r"count"), maximum=0)

    def test_coerces_maximum_to_an_integer(self, session):
        session.visit("/with_count")
        assert session.has_text("count", maximum="2")
        assert not session.has_text("count", maximum="1")

    def test_is_true_when_text_occurs_same_or_more_times_than_given(self, session):
        session.visit("/with_count")
        assert session.has_text("count", minimum=2)
        assert session.has_text(re.compile(r"count"), minimum=0)

    def test_is_false_when_text_occurs_fewer_times_than_given(self, session):
        session.visit("/with_count")
        assert not session.has_text("count", minimum=3)

    def test_coerces_minimum_to_an_integer(self, session):
        session.visit("/with_count")
        assert session.has_text("count", minimum="2")
        assert not session.has_text("count", minimum="3")

    @pytest.mark.requires("js")
    def test_finds_element_if_it_appears_before_given_wait_duration(self, session):
        with capybara.using_wait_time(0.1):
            session.visit("/with_js")
            session.click_link("Click me")
            assert session.has_text("Has been clicked", wait=0.9)


class TestHasNoText:
    def test_is_false_if_the_given_text_is_on_the_page_at_least_once(self, session):
        session.visit("/with_html")
        assert not session.has_no_text("est")
        assert not session.has_no_text("Lorem")
        assert not session.has_no_text("Redirect")

    def test_is_false_if_scoped_to_an_element_which_has_the_text(self, session):
        session.visit("/with_html")
        with session.scope("//a[@title='awesome title']"):
            assert not session.has_no_text("labore")

    def test_is_true_if_scoped_to_an_element_which_does_not_have_the_text(self, session):
        session.visit("/with_html")
        with session.scope("//a[@title='awesome title']"):
            assert session.has_no_text("monkey")

    def test_ignores_tags(self, session):
        session.visit("/with_html")
        assert session.has_no_text("""exercitation <a href="/foo" id="foo">ullamco</a> laboris""")
        assert not session.has_no_text("exercitation ullamco laboris")

    def test_is_true_if_the_given_text_is_not_on_the_page(self, session):
        session.visit("/with_html")
        assert session.has_no_text("xxxxyzzz")
        assert session.has_no_text("monkey")

    def test_handles_single_quotes_in_the_text(self, session):
        session.visit("/with-quotes")
        assert not session.has_no_text("can't")

    def test_handles_double_quotes_in_the_text(self, session):
        session.visit("/with-quotes")
        assert not session.has_no_text("\"you can't do that.\"")

    def test_is_true_if_text_is_in_the_title_tag_in_the_head(self, session):
        session.visit("/with_js")
        assert session.has_no_text("with_js")

    def test_is_true_if_text_is_inside_a_script_tag_in_the_body(self, session):
        session.visit("/with_js")
        assert session.has_no_text("a javascript comment")
        assert session.has_no_text("aVar")

    def test_is_true_if_the_given_text_is_on_the_page_but_not_visible(self, session):
        session.visit("/with_html")
        assert session.has_no_text("Inside element with hidden ancestor")

    def test_is_false_if_all_given_and_text_is_invisible(self, session):
        session.visit("/with_html")
        assert not session.has_no_text("all", "Some of this text is hidden!")

    def test_is_false_if_capybara_ignore_hidden_elements_is_false_and_text_is_invisible(self, session):
        capybara.ignore_hidden_elements = False
        session.visit("/with_html")
        assert not session.has_no_text("Some of this text is hidden!")

    def test_is_true_if_the_text_in_the_page_does_not_match_given_regex(self, session):
        session.visit("/with_html")
        assert session.has_no_text(re.compile(r"xxxxyzzz"))

    def test_is_false_if_the_text_in_the_page_matches_given_regex(self, session):
        session.visit("/with_html")
        assert not session.has_no_text(re.compile(r"Lorem"))

    def test_escapes_any_characters_that_would_have_special_meaning_in_a_regex(self, session):
        session.visit("/with_html")
        assert session.has_no_text(".orem")

    @pytest.mark.requires("js")
    def test_waits_for_text_to_disappear(self, session):
        session.visit("/with_js")
        session.click_link("Click me")
        assert session.has_no_text("I changed it")

    @pytest.mark.requires("js")
    def test_does_not_find_element_if_it_appears_after_given_wait_duration(self, session):
        session.visit("/with_js")
        session.click_link("Click me")
        assert session.has_no_text("Has been clicked", wait=0.1)
