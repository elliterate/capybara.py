from capybara.selector.selector import add_selector, remove_selector, selectors


__all__ = ["add_selector", "remove_selector", "selectors"]


with add_selector("xpath") as s:
    s.xpath = lambda xpath: xpath
