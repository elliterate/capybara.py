from xpath import dsl as x

import capybara
from capybara.helpers import desc
from capybara.selector.filter_set import add_filter_set, remove_filter_set, filter_sets
from capybara.selector.selector import add_selector, remove_selector, selectors
from capybara.utils import isregex


__all__ = ["add_filter_set", "add_selector", "filter_sets", "remove_filter_set", "remove_selector", "selectors"]


with add_selector("css") as s:
    s.css = lambda css: css

with add_selector("xpath") as s:
    s.xpath = lambda xpath: xpath

with add_selector("id") as s:
    @s.xpath
    def xpath(id):
        return x.descendant()[x.attr("id") == id]

with add_filter_set("field") as fs:
    @fs.filter("checked", boolean=True)
    def checked(node, value):
        return not node.checked ^ value

    @fs.filter("disabled", boolean=True, default=False, skip_if="all")
    def disabled(node, value):
        return not node.disabled ^ value

    @fs.filter("readonly", boolean=True)
    def readonly(node, value):
        return not node.readonly ^ value

    @fs.filter("unchecked", boolean=True)
    def unchecked(node, value):
        return node.checked ^ value

    @fs.describe
    def describe(options):
        description, states = "", []

        if options.get("checked") or options.get("unchecked") is False:
            states.append("checked")
        if options.get("unchecked") or options.get("checked") is False:
            states.append("not checked")
        if options.get("disabled") is True:
            states.append("disabled")

        if states:
            description += " that is {}".format(" and ".join(states))

        return description

with add_selector("button") as s:
    @s.xpath
    def xpath(locator):
        input_button_expr = x.descendant("input")[
            x.attr("type").one_of("submit", "reset", "image", "button")]
        button_expr = x.descendant("button")
        image_button_expr = x.descendant("input")[x.attr("type").equals("image")]

        attr_matchers = (
            x.attr("id").equals(locator) |
            x.attr("value").is_(locator) |
            x.attr("title").is_(locator))
        image_attr_matchers = x.attr("alt").is_(locator)

        if capybara.enable_aria_label:
            attr_matchers |= x.attr("aria-label").is_(locator)
            image_attr_matchers |= x.attr("aria-label").is_(locator)

        input_button_expr = input_button_expr[attr_matchers]
        button_expr = button_expr[
            attr_matchers |
            x.string.n.is_(locator) |
            x.descendant("img")[x.attr("alt").is_(locator)]]
        image_button_expr = image_button_expr[image_attr_matchers]

        return input_button_expr + button_expr + image_button_expr

    @s.filter("disabled", boolean=True, default=False, skip_if="all")
    def disabled(node, value):
        return not node.disabled ^ value

    @s.describe
    def describe(options):
        description = ""
        if options.get("disabled") is True:
            description += " that is disabled"
        return description

with add_selector("checkbox") as s:
    @s.xpath
    def xpath(locator):
        expr = x.descendant("input")[x.attr("type").equals("checkbox")]
        expr = _locate_field(expr, locator)
        return expr

    s.filter_set("field")

with add_selector("field") as s:
    @s.xpath
    def xpath(locator):
        expr = x.descendant("input", "select", "textarea")[
            ~x.attr("type").one_of("hidden", "image", "submit")]
        expr = _locate_field(expr, locator)
        return expr

    s.filter_set("field")

with add_selector("fieldset") as s:
    @s.xpath
    def xpath(locator):
        expr = x.descendant("fieldset")
        expr = expr[
            x.attr("id").equals(locator) |
            x.child("legend")[x.string.n.is_(locator)]]
        return expr

with add_selector("file_field") as s:
    s.label = "file field"

    @s.xpath
    def xpath(locator):
        expr = x.descendant("input")[x.attr("type").equals("file")]
        expr = _locate_field(expr, locator)
        return expr

    s.filter_set("field")

with add_selector("fillable_field") as s:
    s.label = "field"

    @s.xpath
    def xpath(locator):
        expr = x.descendant("input", "textarea")[
            ~x.attr("type").one_of("checkbox", "file", "hidden", "image", "radio", "submit")]
        expr = _locate_field(expr, locator)
        return expr

    s.filter_set("field")

with add_selector("frame") as s:
    @s.xpath
    def xpath(locator):
        expr = x.descendant("frame") + x.descendant("iframe")
        expr = expr[x.attr("id").equals(locator) | x.attr("name").equals(locator)]
        return expr

with add_selector("label") as s:
    @s.xpath
    def xpath(locator):
        expr = x.descendant("label")
        if locator:
            expr = expr[x.string.n.is_(str(locator)) | x.attr("id").equals(str(locator))]
        return expr

    @s.filter("field")
    def field(node, field_or_value):
        from capybara.node.element import Element

        if isinstance(field_or_value, Element):
            if field_or_value["id"] and field_or_value["id"] == node["for"]:
                return True
            else:
                return node.base in field_or_value._find_xpath("./ancestor::label[1]")
        else:
            return node["for"] == str(field_or_value)

    @s.describe
    def describe(options):
        description = ""
        if options.get("field"):
            description += " for {}".format(options["field"])
        return description

with add_selector("link") as s:
    @s.xpath
    def xpath(locator):
        expr = x.descendant("a")[x.attr("href")]

        attr_matchers = (
            x.attr("id").equals(locator) |
            x.attr("title").is_(locator) |
            x.string.n.is_(locator))

        if capybara.enable_aria_label:
            attr_matchers |= x.attr("aria-label").is_(locator)

        expr = expr[
            attr_matchers |
            x.descendant("img")[x.attr("alt").is_(locator)]]

        return expr

    @s.filter("href")
    def href(node, href):
        if isregex(href):
            return bool(href.search(node["href"]))
        else:
            # For href element attributes, Selenium returns the full URL that would
            # be visited rather than the raw value in the source. So we use XPath.
            query = x.axis("self")[x.attr("href") == str(href)]
            return node.has_selector("xpath", query)

    @s.describe
    def describe(options):
        description = ""
        if options.get("href"):
            description += " with href {}".format(desc(options["href"]))
        return description

with add_selector("link_or_button") as s:
    s.label = "link or button"

    @s.xpath
    def xpath(locator):
        return selectors["link"](locator) + selectors["button"](locator)

    @s.filter("disabled", boolean=True, default=False, skip_if="all")
    def disabled(node, value):
        return (
            node.tag_name == "a" or
            not node.disabled ^ value)

    @s.describe
    def describe(options):
        description = ""
        if options.get("disabled") is True:
            description += " that is disabled"
        return description

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

    s.filter_set("field")

with add_selector("select") as s:
    s.label = "select box"

    @s.xpath
    def xpath(locator):
        expr = x.descendant("select")
        expr = _locate_field(expr, locator)
        return expr

    s.filter_set("field")

    @s.filter("multiple", boolean=True)
    def multiple(node, value):
        return not node.multiple ^ value

    @s.filter("options")
    def options(node, options):
        if node.visible:
            actual = [n.text for n in node.find_all("xpath", ".//option")]
        else:
            actual = [n.all_text for n in node.find_all("xpath", ".//option", visible=False)]

        return sorted(options) == sorted(actual)

    @s.filter("selected")
    def selected(node, selected):
        if not isinstance(selected, list):
            selected = [selected]

        actual = [
            n.all_text
            for n in node.find_all("xpath", ".//option", visible=False)
            if n.selected]

        return sorted(selected) == sorted(actual)

    @s.filter("with_options")
    def with_options(node, options):
        finder_settings = {"minimum": 0}
        if not node.visible:
            finder_settings["visible"] = False

        return all([
            node.find_first("option", option, **finder_settings)
            for option in options])

    @s.describe
    def describe(options):
        description = ""

        if options.get("multiple") is True:
            description += " with the multiple attribute"
        if options.get("multiple") is False:
            description += " without the multiple attribute"
        if options.get("options"):
            description += " with options {}".format(desc(options["options"]))
        if options.get("selected"):
            description += " with {} selected".format(desc(options["selected"]))
        if options.get("with_options"):
            description += " with at least options {}".format(desc(options["with_options"]))

        return description

with add_selector("table") as s:
    @s.xpath
    def xpath(locator):
        expr = x.descendant("table")
        expr = expr[
            x.attr("id").equals(locator) |
            x.descendant("caption").is_(locator)]
        return expr


def _locate_field(field_expr, locator):
    attr_matchers = (
        x.attr("id").equals(locator) |
        x.attr("name").equals(locator) |
        x.attr("placeholder").equals(locator) |
        x.attr("id").equals(x.anywhere("label")[x.string.n.is_(locator)].attr("for")))

    if capybara.enable_aria_label:
        attr_matchers |= x.attr("aria-label").is_(locator)

    expr = field_expr[attr_matchers]
    expr += x.descendant("label")[x.string.n.is_(locator)].descendant(field_expr)

    return expr
