from warnings import warn

import capybara
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
        return "<capybara.node.element.Element tag=\"{tag}\" path=\"{path}\">".format(
            tag=self.tag_name,
            path=self.path)

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
    def visible(self):
        """ bool: Whether or not the element is visible. """
        return self.base.visible

    @property
    @synchronize
    def value(self):
        """ str: The value of the form element. """
        return self.base.value

    @property
    def text(self):
        """
        Retrieve the text of the element. If :data:`capybara.ignore_hidden_elements` is ``True``,
        which it is by default, then this will return only text which is visible. The exact
        semantics of this may differ between drivers, but generally any text within elements with
        ``display: none`` is ignored.

        Returns:
            str: The text of the element.
        """

        if capybara.ignore_hidden_elements or capybara.visible_text_only:
            return self.visible_text
        else:
            return self.all_text

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

    @property
    @synchronize
    def readonly(self):
        """ bool: Whether or not the element is readonly. """
        return self.base.readonly

    @property
    @synchronize
    def multiple(self):
        """ bool: Whether or not the element supports multiple results. """
        return self.base.multiple

    @property
    @synchronize
    def path(self):
        """ str: An XPath expression describing where on the page the element can be found. """
        return self.base.path

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
    def double_click(self):
        """ Double-click the element. """
        self.base.double_click()

    @synchronize
    def drag_to(self, node):
        """
        Drag the element to the given other element. ::

            source = page.find("#foo")
            target = page.find("#bar")
            source.drag_to(target)

        Args:
            node (Element): The element to drag to.
        """

        self.base.drag_to(node.base)

    @synchronize
    def send_keys(self, *args):
        """
        Send keystrokes to the element.

        Examples::

            from selenium.webdriver.common.keys import Keys

            element.send_keys("foo")                  # => value: "foo"
            element.send_keys("tet", Keys.LEFT, "s")  # => value: "test"

        Args:
            *args: Variable length list of keys to send.
        """

        self.base.send_keys(*args)

    @synchronize
    def hover(self):
        """ Hover on the element. """
        self.base.hover()

    @synchronize
    def right_click(self):
        """ Right-click the element. """
        self.base.right_click()

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
