class ActionsMixin(object):
    def click_link(self, locator, **kwargs):
        """
        Finds a link by id, text, or title and clicks it. Also looks at image alt text inside the
        link.

        Args:
            locator (str): Text, id, title, or nested image's alt attribute.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.
        """

        return self.find("link", locator, **kwargs).click()
