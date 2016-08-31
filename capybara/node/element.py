from warnings import warn

from capybara.node.base import Base, synchronize


class Element(Base):
    """
    An :class:`Element` represents a single element on the page. It is possible to interact with the
    contents of this element the same as with a document::

        session = Session("selenium", my_app)

        bar = session.find("#bar")       # from capybara.node.finders.FindersMixin
        bar.select("Baz", field="Quox")  # from capybara.node.actions.ActionsMixin

    :class:`Element` also has access to HTML attributes and other properties of the element::

        bar.value
        bar.text
        bar["title"]
    """

    def __init__(self, session, base, query_scope, query):
        super(type(self), self).__init__(session, base)
        self.query_scope = query_scope
        self.query = query

    def __repr__(self):
        return "<capybara.node.element.Element tag=\"{tag}\">".format(
            tag=self.tag_name)

    @property
    def native(self):
        """ object: The native element from the driver. """
        return self.base.native

    def reload(self):
        if self.allow_reload:
            query_scope = self.query_scope.reload()
            reloaded = query_scope.find_first(
                self.query.name, self.query.locator, **self.query.kwargs)
            if reloaded:
                self.base = reloaded.base
        return self

    @property
    @synchronize
    def tag_name(self):
        """ str: The tag name of the element. """
        return self.base.tag_name

    @property
    @synchronize
    def value(self):
        """ str: The value of the form element. """
        return self.base.value

    @property
    def text(self):
        """ str: The text of the element. """
        return self.visible_text

    @property
    @synchronize
    def all_text(self):
        """ str: All of the text of the element. """
        return self.base.all_text

    @property
    @synchronize
    def visible_text(self):
        """ str: Only the visible text of the element. """
        return self.base.visible_text

    @property
    @synchronize
    def checked(self):
        """ bool: Whether or not the element is checked. """
        return self.base.checked

    @property
    @synchronize
    def selected(self):
        """ bool: Whether or not the element is selected. """
        return self.base.selected

    @property
    @synchronize
    def disabled(self):
        """ bool: Whether or not the element is disabled. """
        return self.base.disabled

    @synchronize
    def __getitem__(self, name):
        """
        Retrieve the given attribute. ::

            element["title"]  # => HTML title attribute

        Args:
            name (str): The attribute to retrieve.

        Returns:
            str: The value of the attribute.
        """

        return self.base[name]

    @synchronize
    def click(self):
        """ Click the element. """
        self.base.click()

    @synchronize
    def select_option(self):
        """ Select this node if it is an option element inside a select tag. """
        if self.disabled:
            warn("Attempt to select disabled option: {}".format(self.value or self.text))
        self.base.select_option()

    @synchronize
    def set(self, value):
        """
        Set the value of the form element to the given value.

        Args:
            value (bool | str): The new value.
        """

        self.base.set(value)

    @synchronize
    def unselect_option(self):
        """ Unselect this node if it is an option element inside a multiple select tag. """
        self.base.unselect_option()
