class TestHasText:
    def test_is_true_if_the_given_text_is_on_the_page_at_least_once(self, session):
        session.visit("/with_html")
        assert session.has_text("est")
        assert session.has_text("Lorem")
        assert session.has_text("Redirect")

    def test_ignores_tags(self, session):
        session.visit("/with_html")
        assert not session.has_text("""exercitation <a href="/foo">ullamco</a> laboris""")
        assert session.has_text("exercitation ullamco laboris")

    def test_ignores_extra_whitespace_and_newlines(self, session):
        session.visit("/with_html")
        assert session.has_text("text with whitespace")

    def test_ignores_white_space_and_newlines_in_the_search_string(self, session):
        session.visit("/with_html")
        assert session.has_text("text     with \n\n whitespace")

    def test_is_false_if_the_given_text_is_not_on_the_page(self, session):
        session.visit("/with_html")
        assert not session.has_text("xxxxyzzz")
        assert not session.has_text("monkey")

    def test_handles_single_quotes_in_the_text(self, session):
        session.visit("/with-quotes")
        assert session.has_text("can't")

    def test_handles_double_quotes_in_the_text(self, session):
        session.visit("/with-quotes")
        assert session.has_text("\"No,\" he said")

    def test_handles_mixed_single_and_double_quotes_in_the_text(self, session):
        session.visit("/with-quotes")
        assert session.has_text("\"you can't do that.\"")

    def test_is_false_if_text_is_in_the_title_tag_in_the_head(self, session):
        session.visit("/with_js")
        assert not session.has_text("with_js")

    def test_is_false_if_text_is_inside_a_script_tag_in_the_body(self, session):
        session.visit("/with_js")
        assert not session.has_text("a javascript comment")
        assert not session.has_text("aVar")

    def test_accepts_non_string_parameters(self, session):
        session.visit("/with_html")
        assert session.has_text(42)

    def test_is_true_when_passed_none(self, session):
        session.visit("/with_html")
        assert session.has_text(None)

    def test_waits_for_text_to_appear(self, session):
        session.visit("/with_js")
        session.click_link("Click me")
        assert session.has_text("Has been clicked")
