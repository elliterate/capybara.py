import pytest

from capybara.exceptions import ElementNotFound


class TestFindByID:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    def test_finds_any_element_by_id(self, session):
        assert session.find_by_id("red").tag_name == "a"

    def test_raises_an_error_if_no_element_with_id_is_found(self, session):
        with pytest.raises(ElementNotFound):
            session.find_by_id("nothing_with_this_id")

    def test_finds_invisible_elements_when_visible_is_false(self, session):
        assert "with hidden ancestor" in session.find_by_id("hidden_via_ancestor", visible=False).all_text

    def test_does_not_find_invisible_elements_when_visible_is_true(self, session):
        with pytest.raises(ElementNotFound):
            session.find_by_id("hidden_via_ancestor", visible=True)
