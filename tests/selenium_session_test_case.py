import pytest


class SeleniumSessionTestCase:
    @pytest.fixture(scope="module")
    def session(self):
        raise NotImplementedError()

    @pytest.fixture(autouse=True)
    def reset_session(self, session):
        try:
            yield
        finally:
            session.reset()

    def test_fill_in_with_clear_backspace_fills_in_a_field_replacing_an_existing_value(self, session):
        session.visit("/form")
        session.fill_in("form_first_name", value="Harry", fill_options={"clear": "backspace"})
        assert session.find("fillable_field", "form_first_name").value == "Harry"

    def test_fill_in_with_clear_backspace_only_triggers_onchange_once(self, session):
        session.visit("/with_js")
        session.fill_in(
            "with_change_event", value="some value", fill_options={"clear": "backspace"})
        # click outside the field to trigger the change event
        session.find("css", "body").click()
        assert session.find(
            "css", ".change_event_triggered", match="one", wait=5).has_text("some value")

    def test_fill_in_with_clear_backspace_triggers_change_when_clearing_field(self, session):
        session.visit("/with_js")
        session.fill_in("with_change_event", value="", fill_options={"clear": "backspace"})
        # click outside the field to trigger the change event
        session.find("css", "body").click()
        assert session.has_selector("css", ".change_event_triggered", match="one", wait=5)

    def test_fill_in_with_clear_backspace_triggers_input_event_field_value_length_times(self, session):
        session.visit("/with_js")
        session.fill_in("with_change_event", value="", fill_options={"clear": "backspace"})
        # click outside the field to trigger the change event
        session.find("css", "body").click()
        assert session.has_xpath("//p[@class='input_event_triggered']", count=13)

    def test_repr_outputs_obsolete_elements(self, session):
        session.visit("/form")
        el = session.find("button", "Click me!")
        el.click()
        assert session.has_no_button("Click me!")
        assert repr(el) == "Obsolete <capybara.node.element.Element>"
