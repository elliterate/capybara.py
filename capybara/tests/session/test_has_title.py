import pytest


class TestHasTitle:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_js")

    def test_is_true_if_the_page_has_the_given_title(self, session):
        assert session.has_title("with_js")

    @pytest.mark.requires("js")
    def test_waits_for_title(self, session):
        session.click_link("Change title")
        assert session.has_title("changed title")

    def test_is_false_if_the_page_does_not_have_the_given_title(self, session):
        assert not session.has_title("monkey")

    def test_defaults_to_exact_false_matching(self, session):
        assert session.has_title("with_js")
        assert session.has_title("with_")

    def test_matches_exactly_if_exact_true_option_passed(self, session):
        assert session.has_title("with_js", exact=True)
        assert not session.has_title("with_", exact=True)

    def test_matches_partial_if_exact_false_option_passed(self, session):
        assert session.has_title("with_js", exact=False)
        assert session.has_title("with_", exact=False)


class TestHasNoTitle:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_js")

    def test_is_false_if_the_page_has_the_given_title(self, session):
        assert session.has_no_title("with_js") is False

    @pytest.mark.requires("js")
    def test_waits_for_title_to_disappear(self, session):
        session.click_link("Change title")
        assert session.has_no_title("with_js") is True

    def test_is_true_if_the_page_does_not_have_the_given_title(self, session):
        assert session.has_no_title("monkey") is True
