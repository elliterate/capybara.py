from xpath import dsl as x

from capybara.selector.selector import add_selector, remove_selector, selectors


__all__ = ["add_selector", "remove_selector", "selectors"]


with add_selector("css") as s:
    s.css = lambda css: css

with add_selector("xpath") as s:
    s.xpath = lambda xpath: xpath

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
