import pytest
from time import sleep

import capybara
from capybara.exceptions import ReadOnlyElementError
from capybara.tests.helpers import extract_results, ismarionette


class NodeTestCase:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")


class TestNode(NodeTestCase):
    def test_acts_like_a_session_object(self, session):
        session.visit("/form")
        form = session.find("css", "#get-form")
        assert form.has_field("Middle Name")
        assert form.has_no_field("Languages")
        form.fill_in("Middle Name", value="Monkey")
        form.click_button("med")
        assert extract_results(session)["form[middle_name]"] == "Monkey"

    def test_scopes_css_selectors(self, session):
        assert not session.find("css", "#second").has_css("h1")


class TestNodeQueryScope(NodeTestCase):
    def test_returns_a_reference_to_the_element_the_query_was_evaluated_on(self, session):
        node = session.find("css", "#first")
        assert node.query_scope == node.session.document
        assert node.find("css", "#foo").query_scope == node


class TestNodeText(NodeTestCase):
    def test_extracts_node_text(self, session):
        assert session.find_all("//a")[0].text == "labore"
        assert session.find_all("//a")[1].text == "ullamco"

    def test_returns_document_text_on_html_selector(self, session):
        session.visit("/with_simple_html")
        assert session.find("/html").text == "Bar"


class TestNodeAttribute(NodeTestCase):
    def test_extracts_node_attributes(self, session):
        assert session.find_all("//a")[0]["class"] == "simple"
        assert session.find_all("//a")[1]["id"] == "foo"
        assert session.find_all("//input")[0]["type"] == "text"

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
        assert session.find_first("//input").value == "monkey"
        session.find_first("//input").set("gorilla")
        assert session.find_first("//input").value == "gorilla"

    @pytest.mark.requires("js")
    def test_fills_the_field_even_if_the_caret_was_not_at_the_end(self, session):
        session.execute_script(
            "var el = document.getElementById('test_field');"
            "el.focus();"
            "el.setSelectionRange(0, 0);")
        session.find_first("//input").set("")
        assert session.find_first("//input").value == ""

    def test_raises_if_the_text_field_is_readonly(self, session):
        assert session.find_first("//input[@readonly]").value == "should not change"
        with pytest.raises(ReadOnlyElementError):
            session.find_first("//input[@readonly]").set("changed")
        assert session.find_first("//input[@readonly]").value == "should not change"

    def test_raises_if_the_textarea_is_readonly(self, session):
        assert session.find_first("//textarea[@readonly]").value == "textarea should not change"
        with pytest.raises(ReadOnlyElementError):
            session.find_first("//textarea[@readonly]").set("changed")
        assert session.find_first("//textarea[@readonly]").value == "textarea should not change"

    @pytest.mark.requires("js")
    def test_allows_me_to_change_the_contents_of_a_contenteditable_element(self, session):
        session.visit("/with_js")
        session.find("css", "#existing_content_editable").set("WYSIWYG")
        assert session.find("css", "#existing_content_editable").text == "WYSIWYG"

    @pytest.mark.requires("js")
    def test_allows_me_to_set_the_contents_of_a_contenteditable_element(self, session):
        session.visit("/with_js")
        session.find("css", "#blank_content_editable").set("WYSIWYG")
        assert session.find("css", "#blank_content_editable").text == "WYSIWYG"


class TestNodeTagName(NodeTestCase):
    def test_extracts_node_tag_name(self, session):
        assert session.find_all("//a")[0].tag_name == "a"
        assert session.find_all("//a")[1].tag_name == "a"
        assert session.find_all("//p")[0].tag_name == "p"


class TestNodeDisabled(NodeTestCase):
    def test_extracts_disabled_node(self, session):
        session.visit("/form")
        assert session.find("//input[@id='customer_name']").disabled
        assert not session.find("//input[@id='customer_email']").disabled

    def test_sees_disabled_options_as_disabled(self, session):
        session.visit("/form")
        assert not session.find("//select[@id='form_title']/option[1]").disabled
        assert session.find("//select[@id='form_title']/option[@disabled]").disabled

    def test_sees_enabled_options_in_disabled_select_as_disabled(self, session):
        session.visit("/form")
        assert session.find("//select[@id='form_disabled_select']/option").disabled
        assert not session.find("//select[@id='form_title']/option[1]").disabled

    def test_is_boolean(self, session):
        session.visit("/form")
        assert session.find("//select[@id='form_disabled_select']/option").disabled is True
        assert session.find("//select[@id='form_disabled_select2']/option").disabled is True
        assert session.find("//select[@id='form_title']/option[1]").disabled is False


class TestNodeVisible(NodeTestCase):
    def test_extracts_node_visibility(self, session):
        capybara.ignore_hidden_elements = False
        assert session.find_first("//a").visible
        assert not session.find("//div[@id='hidden']").visible
        assert not session.find("//div[@id='hidden_via_ancestor']").visible
        assert not session.find("//div[@id='hidden_attr']").visible
        assert not session.find("//a[@id='hidden_attr_via_ancestor']").visible
        assert not session.find("//input[@id='hidden_input']").visible

    def test_is_boolean(self, session):
        capybara.ignore_hidden_elements = False
        assert session.find_first("//a").visible is True
        assert session.find("//div[@id='hidden']").visible is False


class TestNodeChecked(NodeTestCase):
    def test_extracts_node_checked_state(self, session):
        session.visit("/form")
        assert session.find("//input[@id='gender_female']").checked is True
        assert session.find("//input[@id='gender_male']").checked is False
        assert session.find_first("//h1").checked is False


class TestNodeSelected(NodeTestCase):
    def test_extracts_node_selected_state(self, session):
        session.visit("/form")
        assert session.find("//option[@value='en']").selected is True
        assert session.find("//option[@value='sv']").selected is False
        assert session.find_first("//h1").checked is False


class TestNodeEquals(NodeTestCase):
    def test_is_true_for_the_same_element(self, session):
        assert session.find("//h1") == session.find("//h1")

    def test_is_false_for_different_elements(self, session):
        assert session.find("//h1") != session.find_first("//p")

    def test_is_false_for_unrelated_objects(self, session):
        assert session.find("//h1") != "Not a node"


class TestNodePath(NodeTestCase):
    def test_returns_xpath_which_points_to_itself(self, session):
        session.visit("/path")
        element = session.find("link", "Second Link")
        assert session.find("xpath", element.path) == element


@pytest.mark.requires("js", "drag")
class TestNodeDragTo(NodeTestCase):
    def test_drags_and_drops_an_object(self, session):
        session.visit("/with_js")
        element = session.find("//div[@id='drag']")
        target = session.find("//div[@id='drop']")
        element.drag_to(target)
        assert session.find("//div[contains(., 'Dropped!')]")


@pytest.mark.requires("hover")
class TestNodeHover(NodeTestCase):
    def test_allows_hovering_on_an_element(self, session):
        session.visit("/with_hover")
        assert not session.find("css", ".hidden_until_hover", visible=False).visible
        session.find("css", ".wrapper").hover()
        assert session.find("css", ".hidden_until_hover", visible=False).visible


class TestNodeClick(NodeTestCase):
    def test_does_not_follow_a_link_if_no_href(self, session):
        session.find("css", "#link_placeholder").click()
        assert session.current_url.endswith("/with_html")

    def test_is_able_to_check_a_checkbox(self, session):
        session.visit("/form")
        checkbox = session.find("checkbox", "form_terms_of_use")
        assert not checkbox.checked
        checkbox.click()
        assert checkbox.checked

    def test_is_able_to_uncheck_a_checkbox(self, session):
        session.visit("/form")
        checkbox = session.find("checkbox", "form_pets_dog")
        assert checkbox.checked
        checkbox.click()
        assert not checkbox.checked

    def test_is_able_to_select_a_radio_button(self, session):
        session.visit("/form")
        radio = session.find("radio_button", "gender_male")
        assert not radio.checked
        radio.click()
        assert radio.checked

    def test_handles_fixed_headers_and_footers(self, session):
        session.visit("/with_fixed_header_footer")
        # session.click_link("Go to root")
        session.find("link", "Go to root").click()
        assert session.has_current_path("/")


@pytest.mark.requires("js")
class TestNodeDoubleClick(NodeTestCase):
    def test_double_clicks_an_element(self, session):
        if ismarionette(session):
            pytest.skip("selenium/geckodriver doesn't support double-click")

        session.visit("/with_js")
        session.find("css", "#click-test").double_click()
        assert session.find("css", "#has-been-double-clicked")


@pytest.mark.requires("js")
class TestNodeRightClick(NodeTestCase):
    def test_right_clicks_an_element(self, session):
        if ismarionette(session):
            pytest.skip("selenium/geckodriver doesn't support right-click")

        session.visit("/with_js")
        session.find("css", "#click-test").right_click()
        assert session.find("css", "#has-been-right-clicked")


@pytest.mark.requires("send_keys")
class TestNodeSendKeys(NodeTestCase):
    def test_sends_a_string_of_keys_to_an_element(self, session):
        session.visit("/form")
        session.find("css", "#address1_city").send_keys("Oceanside")
        assert session.find("css", "#address1_city").value == "Oceanside"

    def test_sends_special_characters(self, session):
        Keys = pytest.importorskip("selenium.webdriver.common.keys").Keys

        if ismarionette(session):
            pytest.skip("selenium/geckodriver doesn't support some special characters")

        session.visit("/form")
        session.find("css", "#address1_city").send_keys(
            "Ocean", Keys.SPACE, "sie", Keys.LEFT, "d")
        assert session.find("css", "#address1_city").value == "Ocean side"


@pytest.mark.requires("js")
class TestNodeReloadWithoutAutomaticReload(NodeTestCase):
    @pytest.fixture(autouse=True)
    def setup_capybara(self):
        capybara.automatic_reload = False

    def test_reloads_the_current_context_of_the_node(self, session):
        session.visit("/with_js")
        node = session.find("css", "#reload-me")
        session.click_link("Reload!")
        sleep(0.3)
        assert node.reload().text == "has been reloaded"
        assert node.text == "has been reloaded"

    def test_reloads_a_parent_node(self, session):
        session.visit("/with_js")
        node = session.find("css", "#reload-me").find("css", "em")
        session.click_link("Reload!")
        sleep(0.3)
        assert node.reload().text == "has been reloaded"
        assert node.text == "has been reloaded"

    def test_does_not_automatically_reload(self, session):
        session.visit("/with_js")
        node = session.find("css", "#reload-me")
        session.click_link("Reload!")
        sleep(0.3)
        with pytest.raises(Exception) as excinfo:
            assert node.has_text("has been reloaded")
        assert isinstance(excinfo.value, session.driver.invalid_element_errors)


@pytest.mark.requires("js")
class TestNodeReloadWithAutomaticReload(NodeTestCase):
    @pytest.fixture(autouse=True)
    def setup_capybara(self):
        capybara.automatic_reload = True

    def test_reloads_the_current_context_of_the_node_automatically(self, session):
        session.visit("/with_js")
        node = session.find("css", "#reload-me")
        session.click_link("Reload!")
        sleep(0.3)
        assert node.text == "has been reloaded"

    def test_reloads_a_parent_node_automatically(self, session):
        session.visit("/with_js")
        node = session.find("css", "#reload-me").find("css", "em")
        session.click_link("Reload!")
        sleep(0.3)
        assert node.text == "has been reloaded"

    def test_reloads_a_node_automatically_when_using_find(self, session):
        session.visit("/with_js")
        node = session.find("css", "#reload-me")
        session.click_link("Reload!")
        sleep(0.3)
        assert node.find("css", "a").text == "has been reloaded"

    def test_does_not_reload_nodes_which_have_not_been_found_with_reevaluatable_queries(self, session):
        session.visit("/with_js")
        node = session.find_all("css", "#the-list li")[1]
        session.click_link("Fetch new list!")
        sleep(0.3)
        with pytest.raises(Exception) as excinfo:
            assert node.has_text("Foo")
        assert isinstance(excinfo.value, session.driver.invalid_element_errors)
        with pytest.raises(Exception) as excinfo:
            assert node.has_text("Bar")
        assert isinstance(excinfo.value, session.driver.invalid_element_errors)

    def test_reloads_nodes_with_options(self, session):
        session.visit("/with_js")
        node = session.find("css", "em", text="reloaded")
        session.click_link("Reload!")
        sleep(1)
        assert node.text == "has been reloaded"
