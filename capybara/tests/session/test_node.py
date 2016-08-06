import pytest


class NodeTestCase:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")


class TestNodeText(NodeTestCase):
    def test_extracts_node_text(self, session):
        assert session.find("xpath", "//a[1]").text == "labore"
        assert session.find("xpath", "//a[2]").text == "ullamco"

    def test_returns_document_text_on_html_selector(self, session):
        session.visit("/with_simple_html")
        assert session.find("xpath", "/html").text == "Bar"
