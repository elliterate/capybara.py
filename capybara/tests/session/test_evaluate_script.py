class TestEvaluateScript:
    def test_evaluates_the_given_script_and_returns_whatever_it_produces(self, session):
        session.visit("/with_js")
        assert session.evaluate_script("1+3") == 4
