class TestExecuteScript:
    def test_executes_the_given_script_and_returns_nothing(self, session):
        session.visit("/with_js")
        assert session.execute_script("document.getElementById('change').textContent = 'Funky Doodle'") is None
        assert session.find("css", "#change").text == "Funky Doodle"

    def test_able_to_call_functions_defined_in_the_page(self, session):
        session.visit("/with_js")
        session.execute_script("$('#change').text('Funky Doodle')")
