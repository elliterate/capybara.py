import pytest
import re


class TestHasCSS:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    def test_is_true_if_the_given_selector_is_on_the_page(self, session):
        assert session.has_css("p")
        assert session.has_css("p a#foo")

    def test_is_false_if_the_given_selector_is_not_on_the_page(self, session):
        assert not session.has_css("abbr")
        assert not session.has_css("p a#doesnotexist")
        assert not session.has_css("p.nosuchclass")

    def test_respects_scopes(self, session):
        with session.scope("//p[@id='first']"):
            assert session.has_css("a#foo")
            assert not session.has_css("a#red")

    @pytest.mark.requires("js")
    def test_waits_for_content_to_appear(self, session):
        session.visit("/with_js")
        session.click_link("Click me")
        assert session.has_css("input[type='submit'][value='New Here']")

    def test_is_true_if_the_content_occurs_within_the_range_given(self, session):
        assert session.has_css("p", between=range(1, 5))
        assert session.has_css("p a#foo", between=range(1, 4))
        assert session.has_css("p a.doesnotexist", between=range(0, 9))

    def test_is_false_if_the_content_occurs_more_or_fewer_times_than_range(self, session):
        assert not session.has_css("p", between=range(6, 12))
        assert not session.has_css("p a#foo", between=range(4, 8))
        assert not session.has_css("p a.doesnotexist", between=range(3, 9))

    def test_is_true_if_the_content_occurs_the_given_number_of_times(self, session):
        assert session.has_css("p", count=3)
        assert session.has_css("p a#foo", count=1)
        assert session.has_css("p a.doesnotexist", count=0)

    def test_is_false_if_the_content_occurs_a_different_number_of_times_than_given(self, session):
        assert not session.has_css("p", count=6)
        assert not session.has_css("p a#foo", count=2)
        assert not session.has_css("p a.doesnotexist", count=1)

    def test_coerces_count_to_an_integer(self, session):
        assert session.has_css("p", count="3")
        assert session.has_css("p a#foo", count="1")

    def test_is_true_when_content_occurs_same_or_fewer_times_than_given(self, session):
        assert session.has_css("h2.head", maximum=5)
        assert session.has_css("h2", maximum=10)
        assert session.has_css("p a.doesnotexist", maximum=1)
        assert session.has_css("p a.doesnotexist", maximum=0)

    def test_is_false_when_content_occurs_more_times_than_given(self, session):
        assert not session.has_css("h2.head", maximum=4)
        assert not session.has_css("h2", maximum=3)
        assert not session.has_css("p", maximum=1)

    def test_coerces_maximum_to_an_integer(self, session):
        assert session.has_css("h2.head", maximum="5")
        assert session.has_css("h2", maximum="10")

    def test_is_true_when_content_occurs_same_or_more_times_than_given(self, session):
        assert session.has_css("h2.head", mimimum=5)
        assert session.has_css("h2", minimum=3)
        assert session.has_css("p a.doesnotexist", minimum=0)

    def test_is_false_when_content_occurs_fewer_times_than_given(self, session):
        assert not session.has_css("h2.head", minimum=6)
        assert not session.has_css("h2", minimum=8)
        assert not session.has_css("p", minimum=10)
        assert not session.has_css("p a.doesnotexist", minimum=1)

    def test_coerces_minimum_to_an_integer(self, session):
        assert session.has_css("h2.head", minimum="5")
        assert session.has_css("h2", minimum="3")

    def test_discards_all_matches_where_the_given_string_is_not_contained(self, session):
        assert session.has_css("p a", text="Redirect", count=1)
        assert not session.has_css("p a", text="Doesnotexist")

    def test_discards_all_matches_where_the_given_regex_is_not_matched(self, session):
        assert session.has_css("p a", text=re.compile("re[dab]i", re.IGNORECASE), count=1)
        assert not session.has_css("p a", text=re.compile("Red$"))


class TestHasNoCSS:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    def test_is_false_if_the_given_selector_is_on_the_page(self, session):
        assert not session.has_no_css("p")
        assert not session.has_no_css("p a#foo")

    def test_is_true_if_the_given_selector_is_not_on_the_page(self, session):
        assert session.has_no_css("abbr")
        assert session.has_no_css("p a#doesnotexist")
        assert session.has_no_css("p.nosuchclass")

    def test_respects_scopes(self, session):
        with session.scope("//p[@id='first']"):
            assert not session.has_no_css("a#foo")
            assert session.has_no_css("a#red")

    @pytest.mark.requires("js")
    def test_waits_for_content_to_disappear(self, session):
        session.visit("/with_js")
        session.click_link("Click me")
        assert session.has_no_css("p#change")

    def test_is_false_if_the_content_occurs_within_the_range_given(self, session):
        assert not session.has_no_css("p", between=range(1, 5))
        assert not session.has_no_css("p a#foo", between=range(1, 4))
        assert not session.has_no_css("p a.doesnotexist", between=range(0, 9))

    def test_is_true_if_the_content_occurs_more_or_fewer_times_than_range(self, session):
        assert session.has_no_css("p", between=range(6, 12))
        assert session.has_no_css("p a#foo", between=range(4, 8))
        assert session.has_no_css("p a.doesnotexist", between=range(3, 9))

    def test_is_false_if_the_content_occurs_the_given_number_of_times(self, session):
        assert not session.has_no_css("p", count=3)
        assert not session.has_no_css("p a#foo", count=1)
        assert not session.has_no_css("p a.doesnotexist", count=0)

    def test_is_true_if_the_content_occurs_a_different_number_of_times_than_given(self, session):
        assert session.has_no_css("p", count=6)
        assert session.has_no_css("p a#foo", count=2)
        assert session.has_no_css("p a.doesnotexist", count=1)

    def test_coerces_count_to_an_integer(self, session):
        assert not session.has_no_css("p", count="3")
        assert not session.has_no_css("p a#foo", count="1")

    def test_is_false_when_content_occurs_same_or_fewer_times_than_given(self, session):
        assert not session.has_no_css("h2.head", maximum=5)
        assert not session.has_no_css("h2", maximum=10)
        assert not session.has_no_css("p a.doesnotexist", maximum=0)

    def test_is_true_when_content_occurs_more_times_than_given(self, session):
        assert session.has_no_css("h2.head", maximum=4)
        assert session.has_no_css("h2", maximum=3)
        assert session.has_no_css("p", maximum=1)

    def test_coerces_maximum_to_an_integer(self, session):
        assert not session.has_no_css("h2.head", maximum="5")
        assert not session.has_no_css("h2", maximum="10")

    def test_is_false_when_content_occurs_same_or_more_times_than_given(self, session):
        assert not session.has_no_css("h2.head", mimimum=5)
        assert not session.has_no_css("h2", minimum=3)
        assert not session.has_no_css("p a.doesnotexist", minimum=0)

    def test_is_true_when_content_occurs_fewer_times_than_given(self, session):
        assert session.has_no_css("h2.head", minimum=6)
        assert session.has_no_css("h2", minimum=8)
        assert session.has_no_css("p", minimum=15)
        assert session.has_no_css("p a.doesnotexist", minimum=1)

    def test_coerces_minimum_to_an_integer(self, session):
        assert not session.has_no_css("h2.head", minimum="5")
        assert not session.has_no_css("h2", minimum="3")

    def test_discards_all_matches_where_the_given_string_is_contained(self, session):
        assert not session.has_no_css("p a", text="Redirect", count=1)
        assert session.has_no_css("p a", text="Doesnotexist")

    def test_discards_all_matches_where_the_given_regex_is_matched(self, session):
        assert not session.has_no_css("p a", text=re.compile("re[dab]i", re.IGNORECASE), count=1)
        assert session.has_no_css("p a", text=re.compile("Red$"))
