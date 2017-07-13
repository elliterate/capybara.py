import pytest
import re

from capybara.exceptions import ModalNotFound


@pytest.mark.requires("modals")
class TestAcceptAlert:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_js")

    def test_accepts_the_alert(self, session):
        with session.accept_alert():
            session.click_link("Open alert")
        assert session.has_xpath("//a[@id='open-alert' and @opened='true']")

    def test_raises_an_error_if_no_alert_found(self, session):
        with pytest.raises(ModalNotFound):
            with session.accept_alert():
                pass

    def test_accepts_the_alert_if_the_text_matches(self, session):
        with session.accept_alert("Alert opened"):
            session.click_link("Open alert")
        assert session.has_xpath("//a[@id='open-alert' and @opened='true']")

    def test_accepts_the_alert_if_text_contains_special_regex_characters(self, session):
        with session.accept_alert("opened [*Yay?*]"):
            session.click_link("Open alert")
        assert session.has_xpath("//a[@id='open-alert' and @opened='true']")

    def test_accepts_the_alert_if_the_text_matches_a_regexp(self, session):
        with session.accept_alert(re.compile(r"op.{2}ed")):
            session.click_link("Open alert")
        assert session.has_xpath("//a[@id='open-alert' and @opened='true']")

    def test_raises_an_error_if_the_text_does_not_match(self, session):
        with pytest.raises(ModalNotFound):
            with session.accept_alert("Incorrect Text"):
                session.click_link("Open alert")

    def test_accepts_an_asynchronous_alert(self, session):
        with session.accept_alert():
            session.click_link("Open delayed alert")
        assert session.has_xpath("//a[@id='open-delayed-alert' and @opened='true']")

    def test_allows_adjustment_of_the_delay(self, session):
        with session.accept_alert(wait=4):
            session.click_link("Open slow alert")
        assert session.has_xpath("//a[@id='open-slow-alert' and @opened='true']")
