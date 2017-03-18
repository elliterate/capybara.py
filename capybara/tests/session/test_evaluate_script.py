class TestEvaluateScript:
    def test_evaluates_the_given_script_and_returns_whatever_it_produces(self, session):
        session.visit("/with_js")
        assert session.evaluate_script("1+3") == 4

    def test_passes_arguments_to_the_script(self, session):
        session.visit("/with_js")
        session.evaluate_script("document.getElementById('change').textContent = arguments[0]", "Doodle Funk")
        assert session.has_css("#change", text="Doodle Funk")

    def test_supports_passing_elements_as_arguments_to_the_script(self, session):
        session.visit("/with_js")
        el = session.find("css", "#change")
        session.evaluate_script("arguments[1].textContent = arguments[0]", "Doodle Funk", el)
        assert session.has_css("#change", text="Doodle Funk")
