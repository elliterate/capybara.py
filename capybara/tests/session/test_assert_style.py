import pytest

from capybara.exceptions import ExpectationNotMet


@pytest.mark.requires("css")
class TestAssertStyle:
    def test_is_true_if_the_elements_style_contains_the_given_properties(self, session):
        session.visit("/with_html")
        assert session.find("css", "#first").assert_style({"display": "block"}) is True

    def test_raises_error_if_the_elements_style_does_not_contain_the_given_properties(self, session):
        session.visit("/with_html")
        with pytest.raises(ExpectationNotMet) as excinfo:
            session.find("css", "#first").assert_style({"display": "inline"})
        assert (
            "Expected node to have styles {'display': 'inline'}. "
            "Actual styles were {'display': 'block'}") in str(excinfo.value)

    @pytest.mark.requires("css", "js")
    def test_waits_for_style(self, session):
        session.visit("/with_js")
        el = session.find("css", "#change")
        session.click_link("Change size")
        assert el.assert_style({"font-size": "50px"}, wait=3)
