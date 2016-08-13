import pytest

from capybara.exceptions import ElementNotFound


class TestFindButton:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/form")

    def test_finds_any_button(self, session):
        assert session.find_button("med")["id"] == "mediocre"
        assert session.find_button("crap321").value == "crappy"

    def test_raises_an_error_if_the_button_does_not_exist(self, session):
        with pytest.raises(ElementNotFound):
            session.find_button("Does not exist")
