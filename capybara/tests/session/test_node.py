import pytest

from capybara.tests.helpers import extract_results


class NodeTestCase:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")


class TestNode(NodeTestCase):
    def test_acts_like_a_session_object(self, session):
        session.visit("/form")
        form = session.find("css", "#get-form")
        form.fill_in("Middle Name", value="Monkey")
        form.click_button("med")
        assert extract_results(session)["form[middle_name]"] == "Monkey"

    def test_scopes_css_selectors(self, session):
        assert not session.find("css", "#second").has_css("h1")


class TestNodeText(NodeTestCase):
    def test_extracts_node_text(self, session):
        assert session.find("//a[1]").text == "labore"
        assert session.find("//a[2]").text == "ullamco"

    def test_returns_document_text_on_html_selector(self, session):
        session.visit("/with_simple_html")
        assert session.find("/html").text == "Bar"


class TestNodeAttribute(NodeTestCase):
    def test_extracts_node_attributes(self, session):
        assert session.find("//a[1]")["class"] == "simple"
        assert session.find("//a[2]")["id"] == "foo"
        assert session.find("//input[1]")["type"] == "text"

    def test_extracts_boolean_node_attributes(self, session):
        assert session.find("//input[@id='checked_field']")["checked"]


class TestNodeValue(NodeTestCase):
    def test_allows_retrieval_of_the_value(self, session):
        assert session.find("//textarea[@id='normal']").value == "banana"

    def test_does_not_swallow_extra_newlines_in_textarea(self, session):
        assert session.find("//textarea[@id='additional_newline']").value == "\nbanana"

    def test_does_not_swallow_newlines_for_set_content_in_textarea(self, session):
        session.find("//textarea[@id='normal']").set("\nbanana")
        assert session.find("//textarea[@id='normal']").value == "\nbanana"

    def test_returns_any_html_content_in_textarea(self, session):
        session.find("//textarea[1]").set("some <em>html</em>here")
        assert session.find("//textarea[1]").value == "some <em>html</em>here"

    def test_defaults_to_on_for_checkboxes(self, session):
        session.visit("/form")
        assert session.find("//input[@id='valueless_checkbox']").value == "on"

    def test_defaults_to_on_for_radio_buttons(self, session):
        session.visit("/form")
        assert session.find("//input[@id='valueless_radio']").value == "on"


class TestNodeSet(NodeTestCase):
    def test_allows_assignment_of_field_value(self, session):
        assert session.find("//input[1]").value == "monkey"
        session.find("//input[1]").set("gorilla")
        assert session.find("//input[1]").value == "gorilla"


class TestNodeChecked(NodeTestCase):
    def test_extracts_node_checked_state(self, session):
        session.visit("/form")
        assert session.find("//input[@id='gender_female']").checked is True
        assert session.find("//input[@id='gender_male']").checked is False
        assert session.find("//h1").checked is False


class TestNodeSelected(NodeTestCase):
    def test_extracts_node_selected_state(self, session):
        session.visit("/form")
        assert session.find("//option[@value='en']").selected is True
        assert session.find("//option[@value='sv']").selected is False
        assert session.find("//h1").selected is False
