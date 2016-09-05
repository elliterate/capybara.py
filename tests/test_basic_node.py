import pytest

import capybara
from capybara.selector import add_selector, remove_selector


class TestString:
    @pytest.fixture
    def string(self):
        return capybara.string("""
            <html>
              <head>
                <title>simple_node</title>
              </head>
              <body>
                <svg><title>not document title</title></svg>
                <div id="page">
                  <div id="content">
                    <h1 data="fantastic">Totally awesome</h1>
                    <p>Yes it is</p>
                  </div>

                  <form>
                    <input type="text" name="bleh" disabled="disabled"/>
                    <input type="text" name="meh"/>
                  </form>

                  <div id="footer">
                    <p>c2010</p>
                    <p>Jonas Nicklas</p>
                    <input type="text" name="foo" value="bar"/>
                    <select name="animal">
                      <option>Monkey</option>
                      <option selected="selected">Capybara</option>
                    </select>
                  </div>

                  <div id="hidden" style="display: none">
                    <p id="secret">Secret</p>
                  </div>

                  <section>
                    <div class="subsection"></div>
                  </section>
                </div>
              </body>
            </html>
        """)

    def test_allows_using_matchers(self, string):
        assert string.has_css("#page")
        assert not string.has_css("#does-not-exist")

    def test_allows_using_custom_matchers(self, string):
        with add_selector("lifeform") as s:
            s.xpath = lambda name: "//option[contains(.,'{}')]".format(name)

        assert string.has_selector("id", "page")
        assert not string.has_selector("id", "does-not-exist")
        assert string.has_selector("lifeform", "Monkey")
        assert not string.has_selector("lifeform", "Gorilla")

        remove_selector("lifeform")

    def test_allows_custom_matcher_using_css(self, string):
        with add_selector("section") as s:
            s.css = lambda css_class: "section .{}".format(css_class)

        assert string.has_selector("section", "subsection")
        assert not string.has_selector("section", "section_8")

        remove_selector("section")

    def test_allows_finding_only_visible_nodes(self, string):
        assert len(string.find_all("css", "#secret", visible=True)) == 0
        assert len(string.find_all("css", "#secret", visible=False)) == 1

    def test_allows_finding_elements_and_extracting_text_from_them(self, string):
        assert string.find("//h1").text == "Totally awesome"

    def test_allows_finding_elements_and_extracting_attributes_from_them(self, string):
        assert string.find("//h1")["data"] == "fantastic"

    def test_allows_finding_elements_and_extracting_the_tag_name_from_them(self, string):
        assert string.find("//h1").tag_name == "h1"

    def test_allows_finding_elements_and_extracting_the_value_from_them(self, string):
        assert string.find("//div/input").value == "bar"
        assert string.find("//select").value == "Capybara"

    def test_allows_finding_elements_and_checking_if_they_are_visible(self, string):
        assert string.find("//h1").visible
        assert not string.find("css", "#secret", visible=False).visible

    def test_allows_finding_elements_and_checking_if_they_are_disabled(self, string):
        assert string.find("//form/input[@name='bleh']").disabled
        assert not string.find("//form/input[@name='meh']").disabled

    def test_returns_the_page_title(self, string):
        assert string.title == "simple_node"

    def test_returns_whether_the_page_has_the_given_title(self, string):
        assert string.has_title("simple_node")
        assert not string.has_title("monkey")
