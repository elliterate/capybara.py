class TestReset:
    def test_resets_page_body(self, session):
        session.visit("/with_html")
        assert session.has_text("This is a test")
        assert "This is a test" in session.find(".//h1").text

        session.reset()
        assert "This is a test" not in session.body
        assert not session.has_selector(".//h1")

    def test_handles_modals_during_unload(self, session):
        session.visit("/with_unload_alert")
        assert session.has_selector("css", "div")
        session.reset()
        assert not session.has_selector("xpath", "/html/body/*")

    def test_handles_already_open_modals(self, session):
        session.visit("/with_unload_alert")
        session.click_link("Go away")
        session.reset()
        assert not session.has_selector("xpath", "/html/body/*")
