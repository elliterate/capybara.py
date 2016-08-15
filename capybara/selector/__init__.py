from xpath import dsl as x

from capybara.selector.selector import add_selector, remove_selector, selectors


__all__ = ["add_selector", "remove_selector", "selectors"]


with add_selector("css") as s:
    s.css = lambda css: css

with add_selector("xpath") as s:
    s.xpath = lambda xpath: xpath

with add_selector("id") as s:
    @s.xpath
    def xpath(id):
        return x.descendant()[x.attr("id") == id]

with add_selector("button") as s:
    @s.xpath
    def xpath(locator):
        input_button_expr = x.descendant("input")[
            x.attr("type").one_of("submit", "reset", "image", "button")]
        button_expr = x.descendant("button")
        image_button_expr = x.descendant("input")[x.attr("type").equals("image")]

        input_button_expr = input_button_expr[
            x.attr("id").equals(locator) |
            x.attr("value").is_(locator) |
            x.attr("title").is_(locator)]
        button_expr = button_expr[
            x.attr("id").equals(locator) |
            x.attr("value").is_(locator) |
            x.attr("title").is_(locator) |
            x.string.n.is_(locator)]
        image_button_expr = image_button_expr[
            x.attr("alt").is_(locator)]

        return input_button_expr + button_expr + image_button_expr

with add_selector("checkbox") as s:
    @s.xpath
    def xpath(locator):
        expr = x.descendant("input")[x.attr("type").equals("checkbox")]
        expr = _locate_field(expr, locator)
        return expr

with add_selector("field") as s:
    @s.xpath
    def xpath(locator):
        expr = x.descendant("input", "select", "textarea")[
            ~x.attr("type").one_of("hidden", "image", "submit")]
        expr = _locate_field(expr, locator)
        return expr

with add_selector("fieldset") as s:
    @s.xpath
    def xpath(locator):
        expr = x.descendant("fieldset")
        expr = expr[
            x.attr("id").equals(locator) |
            x.child("legend")[x.string.n.is_(locator)]]
        return expr

with add_selector("fillable_field") as s:
    s.label = "field"

    @s.xpath
    def xpath(locator):
        expr = x.descendant("input", "textarea")[
            ~x.attr("type").one_of("checkbox", "file", "hidden", "image", "radio", "submit")]
        expr = _locate_field(expr, locator)
        return expr

with add_selector("frame") as s:
    @s.xpath
    def xpath(locator):
        expr = x.descendant("frame") + x.descendant("iframe")
        expr = expr[x.attr("id").equals(locator) | x.attr("name").equals(locator)]
        return expr

with add_selector("link") as s:
    @s.xpath
    def xpath(locator):
        expr = x.descendant("a")[x.attr("href")]
        expr = expr[
            x.attr("id").equals(locator) |
            x.attr("title").is_(locator) |
            x.string.n.is_(locator) |
            x.descendant("img")[x.attr("alt").is_(locator)]]
        return expr

with add_selector("link_or_button") as s:
    s.label = "link or button"

    @s.xpath
    def xpath(locator):
        return selectors["link"](locator) + selectors["button"](locator)

with add_selector("option") as s:
    @s.xpath
    def xpath(locator):
        expr = x.descendant("option")
        expr = expr[x.string.n.is_(locator)]
        return expr

with add_selector("radio_button") as s:
    s.label = "radio button"

    @s.xpath
    def xpath(locator):
        expr = x.descendant("input")[x.attr("type").equals("radio")]
        expr = _locate_field(expr, locator)
        return expr

with add_selector("select") as s:
    s.label = "select box"

    @s.xpath
    def xpath(locator):
        expr = x.descendant("select")
        expr = _locate_field(expr, locator)
        return expr

with add_selector("table") as s:
    @s.xpath
    def xpath(locator):
        expr = x.descendant("table")
        expr = expr[
            x.attr("id").equals(locator) |
            x.descendant("caption").is_(locator)]
        return expr


def _locate_field(field_expr, locator):
    expr = field_expr[
        x.attr("id").equals(locator) |
        x.attr("name").equals(locator) |
        x.attr("placeholder").equals(locator) |
        x.attr("id").equals(x.anywhere("label")[x.string.n.is_(locator)].attr("for"))]
    expr += x.descendant("label")[x.string.n.is_(locator)].descendant(field_expr)

    return expr
