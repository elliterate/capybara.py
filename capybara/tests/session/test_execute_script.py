import pytest


@pytest.mark.requires("js")
class TestExecuteScript:
    def test_executes_the_given_script_and_returns_nothing(self, session):
        session.visit("/with_js")
        assert session.execute_script("document.getElementById('change').textContent = 'Funky Doodle'") is None
        assert session.has_css("#change", text="Funky Doodle")

    def test_able_to_call_functions_defined_in_the_page(self, session):
        session.visit("/with_js")
        session.execute_script("$('#change').text('Funky Doodle')")

    def test_passes_arguments_to_the_script(self, session):
        session.visit("/with_js")
        session.execute_script("document.getElementById('change').textContent = arguments[0]", "Doodle Funk")
        assert session.has_css("#change", text="Doodle Funk")

    def test_supports_passing_elements_as_arguments_to_the_script(self, session):
        session.visit("/with_js")
        el = session.find("css", "#change")
        session.execute_script("arguments[1].textContent = arguments[0]", "Doodle Funk", el)
        assert session.has_css("#change", text="Doodle Funk")
