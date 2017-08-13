import pytest

from capybara.node.element import Element
from capybara.tests.helpers import isselenium


@pytest.mark.requires("js")
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

    def test_supports_returning_elements(self, session):
        session.visit("/with_js")
        el = session.evaluate_script("document.getElementById('change')")
        assert isinstance(el, Element)
        assert el == session.find("css", "#change")

    def test_supports_returning_arrays_of_elements(self, session):
        session.visit("/form")
        elements = session.evaluate_script("document.querySelectorAll('#form_city option')")
        for element in elements:
            assert isinstance(element, Element)
        assert elements == list(session.find("css", "#form_city").find_all("css", "option"))

    def test_supports_returning_dicts_with_elements(self, session):
        if isselenium(session):
            pytest.importorskip("selenium", minversion="3.4.3")

        session.visit("/form")
        result = session.evaluate_script(
          "{a: document.getElementById('form_title'), "
          "b: {c: document.querySelectorAll('#form_city option')}}")
        assert result == {
            'a': session.find("id", "form_title"),
            'b': {
                'c': list(session.find("css", "#form_city").find_all("css", "option"))}}
