from xpath import dsl as x

from capybara.selector.selector import add_selector, remove_selector, selectors


__all__ = ["add_selector", "remove_selector", "selectors"]


with add_selector("css") as s:
    s.css = lambda css: css

with add_selector("xpath") as s:
    s.xpath = lambda xpath: xpath

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
