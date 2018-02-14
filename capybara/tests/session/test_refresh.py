import pytest
from time import sleep

from capybara.tests.app import AppError
from capybara.tests.helpers import extract_results


class TestRefresh:
    def test_reloads_the_page(self, session):
        session.visit("/form")
        assert session.has_select("form_locale", selected="English")
        session.select("Swedish", field="form_locale")
        assert session.has_select("form_locale", selected="Swedish")
        session.refresh()
        assert session.has_select("form_locale", selected="English")

    @pytest.mark.requires("server")
    def test_raises_any_errors_caught_inside_the_server(self, session):
        session.visit("/error")
        with pytest.raises(AppError):
            session.refresh()

    def test_reposts(self, session):
        session.visit("/form")
        session.select("Sweden", field="form_region")
        session.click_button("awesome")
        post_count = extract_results(session)["post_count"]

        session.refresh()
        sleep(2)

        results = extract_results(session)
        assert results["post_count"] == post_count + 1
        assert results["form[region]"] == "Sweden"
