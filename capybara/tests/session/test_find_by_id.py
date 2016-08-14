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
