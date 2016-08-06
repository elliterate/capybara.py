import pytest

from capybara.selector import add_selector, remove_selector, selectors


class TestAddSelector:
    @pytest.fixture(autouse=True)
    def teardown_selector(self):
        try:
            yield
        finally:
            remove_selector("custom_selector")

    def test_sets_name(self):
        with add_selector("custom_selector"):
            pass
        selector = selectors["custom_selector"]
        assert selector.name == "custom_selector"

    def test_label_assignment_sets_label(self):
        with add_selector("custom_selector") as s:
            s.label = "My Custom Selector"
        selector = selectors["custom_selector"]
        assert selector.label == "My Custom Selector"

    def test_xpath_assignment_sets_xpath_query_function(self):
        with add_selector("custom_selector") as s:
            s.xpath = lambda id: ".//h1[./@id = '{}']".format(id)
        selector = selectors["custom_selector"]
        assert selector("foo") == ".//h1[./@id = 'foo']"

    def test_xpath_decorator_sets_xpath_query_function(self):
        with add_selector("custom_selector") as s:
            @s.xpath
            def xpath(id):
                return ".//h1[./@id = '{}']".format(id)
        selector = selectors["custom_selector"]
        assert selector("foo") == ".//h1[./@id = 'foo']"

    def test_xpath_decorator_with_parens_sets_xpath_query_function(self):
        with add_selector("custom_selector") as s:
            @s.xpath()
            def xpath(id):
                return ".//h1[./@id = '{}']".format(id)
        selector = selectors["custom_selector"]
        assert selector("foo") == ".//h1[./@id = 'foo']"

    def test_css_assignment_sets_css_query_function(self):
        with add_selector("custom_selector") as s:
            s.css = lambda id: "h1#{}".format(id)
        selector = selectors["custom_selector"]
        assert selector("foo") == "h1#foo"

    def test_css_decorator_sets_css_query_function(self):
        with add_selector("custom_selector") as s:
            @s.css
            def css(id):
                return "h1#{}".format(id)
        selector = selectors["custom_selector"]
        assert selector("foo") == "h1#foo"

    def test_css_decorator_with_parens_sets_css_query_function(self):
        with add_selector("custom_selector") as s:
            @s.css()
            def css(id):
                return "h1#{}".format(id)
        selector = selectors["custom_selector"]
        assert selector("foo") == "h1#foo"


class TestRemoveSelector:
    def test_removes_added_selector(self):
        assert "custom_selector" not in selectors
        with add_selector("custom_selector"):
            pass
        assert "custom_selector" in selectors
        remove_selector("custom_selector")
        assert "custom_selector" not in selectors

    def test_does_not_raise_an_error_for_a_non_existent_selector(self):
        remove_selector("does_not_exist")
