import pytest

from capybara.node.document import Document


class TestCurrentScope:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_scope")

    def test_returns_the_document_when_outside_of_a_scope(self, session):
        assert isinstance(session.current_scope, Document)

    def test_returns_the_element_in_scope(self, session):
        with session.scope("//*[@id='simple_first_name']"):
            assert session.current_scope["name"] == "first_name"

    def test_returns_the_element_in_nested_scope(self, session):
        with session.scope("//div[@id='for_bar']"):
            with session.scope(".//input[@value='Peter']"):
                assert session.current_scope["name"] == "form[first_name]"
