Capybara
========

Capybara helps you test web applications by simulating how a real user would
interact with your app. It is agnostic about the driver running your tests and
comes with Werkzeug and Selenium support built in.

**Need help?** Ask on the mailing list (please do not open an issue on GitHub):
http://groups.google.com/group/capybara-py/.

**Note: Firefox 48+** If you're using Firefox with ``selenium`` and want full
functionality stay on either Firefox |ff45|_ or |ff47|_. If using ``selenium``
3.0+ this will require configuring your driver with the ``"marionette": False``
capability as shown below::

    import capybara

    @capybara.register_driver("selenium")
    def init_selenium_driver(app):
        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

        from capybara.selenium.driver import Driver

        capabilities = DesiredCapabilities.FIREFOX.copy()
        capabilities["marionette"] = False

        return Driver(app, browser="firefox", desired_capabilities=capabilities)

Using Firefox 48+ requires ``geckodriver`` and ``selenium`` v3, the combo of
which currently has multiple issues and is feature incomplete.

.. |ff45| replace:: 45.0esr
.. _ff45: https://ftp.mozilla.org/pub/firefox/releases/45.0esr/
.. |ff47| replace:: 47.0.1
.. _ff47: https://ftp.mozilla.org/pub/firefox/releases/47.0.1/

_`Key benefits`
~~~~~~~~~~~~~~~

- **No setup** necessary for WSGI-compliant applications. Works out of the box.
- **Intuitive API** which mimics the language an actual user would use.
- **Switch the backend** your tests run against from fast headless mode to an
  actual browser with no changes to your tests.
- **Powerful synchronization** features mean you never have to manually wait
  for asynchronous processes to complete.

_`Setup`
~~~~~~~~

To install, add ``capybara-py`` to your application's test requirements.

In your test setup, set :data:`capybara.app` to your WSGI-compliant app::

    import app
    import capybara

    capybara.app = app

_`Using Capybara with pytest`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Load pytest support by adding it to the ``pytest_plugins`` in your
``conftest.py``::

    pytest_plugins = ["capybara.pytest_plugin"]

The plugin provides a :data:`page <capybara.dsl.page>` fixture for use in your
tests::

    def test_user_signs_in(page):
        page.visit("/")
        page.click_link("Sign in")

        page.fill_in("Username", value="user@example.com")
        page.fill_in("Password", value="password")
        page.click_button("Sign in")

Use the ``js`` mark to switch to the :data:`capybara.javascript_driver`
(``"selenium"`` by default), or use the ``driver`` mark to switch to one
specific driver. For example::

    import pytest

    @pytest.mark.js
    def test_uses_the_default_js_driver():
        # ...

    @pytest.mark.driver("selenium")
    def test_switches_to_one_specific_driver():
        # ...

_`Using Capybara with unittest`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Define a base test case that exposes the :data:`page <capybara.dsl.page>` session proxy and cleans
up between tests::

    import capybara
    import capybara.dsl
    import unittest

    class CapybaraTestCase(unittest.TestCase):
        def setUp(self):
            self.page = capybara.dsl.page

        def tearDown(self):
            capybara.reset_sessions()

(Remember to call ``super`` in any subclasses that override ``setUp`` or ``tearDown``!)

_`Drivers`
~~~~~~~~~~

Capybara uses the same DSL to drive a variety of browser and headless drivers.

_`Selecting the Driver`
-----------------------

By default, Capybara uses the ``"werkzeug"`` driver, which is fast but limited:
it does not support JavaScript, nor is it able to access HTTP resources outside
of your WSGI application, such as remote APIs and OAuth services. To get around
these limitations, you can set up a different default driver for your features.
For example if you'd prefer to run everything in Selenium, you could do::

    import capybara

    capybara.default_driver = "selenium"

You can also change the driver temporarily (typically in the setup and teardown
functions)::

    import capybara

    capybara.current_driver = "selenium" # temporarily select different driver
    # tests here
    capybara.use_default_driver()        # switch back to default driver

_`Werkzeug`
-----------

Werkzeug is Capybara's default driver. It is written in pure Python and does
not have any support for executing JavaScript. Since the Werkzeug driver
interacts directly with WSGI interfaces, it does not require a server to be
started. However, this means that if your application is not a WSGI application
(Django, Flask, and most other Python frameworks are WSGI applications) then
you cannot use this driver. Furthermore, you cannot use the Werkzeug driver to
test a remote application, or to access remote URLs (e.g., redirects to
external sites, external APIs, or OAuth services) that your application might
interact with.

_`Selenium`
-----------

At the moment, Capybara supports |selenium_2.0_webdriver|_, *not* Selenium RC.
In order to use Selenium, you'll need to install the ``selenium`` package.
Provided Firefox is installed, everything is set up for you, and you should be
able to start using Selenium right away.

.. |selenium_2.0_webdriver| replace:: Selenium 2.0 (Webdriver)
.. _selenium_2.0_webdriver: http://seleniumhq.org/docs/01_introducing_selenium.html#selenium-2-aka-selenium-webdriver

_`The DSL`
~~~~~~~~~~

_`Navigating`
-------------

You can use the :meth:`visit <capybara.session.Session.visit>` method to navigate to other pages::

    visit("/projects")

The visit method only takes a single parameter, the request method is **always**
GET.

You can get the current path of the browsing session, and test it using the
:meth:`has_current_path <capybara.session_matchers.SessionMatchersMixin.has_current_path>` matcher::

    assert page.has_current_path("/posts/1/comments/2")

**Note:** You can also assert the current path by testing the value of
:attr:`current_path <capybara.session.Session.current_path>` directly. However, using the
:meth:`has_current_path <capybara.session_matchers.SessionMatchersMixin.has_current_path>` matcher
is safer since it uses Capybara's `waiting behavior`_ to ensure that preceding actions (such as a
:meth:`click_link <capybara.node.actions.ActionsMixin.click_link>`) have completed.

.. _waiting behavior: `Asynchronous JavaScript (Ajax and friends)`_

_`Clicking links and buttons`
-----------------------------

*Full reference:* :class:`capybara.node.actions.ActionsMixin`

You can interact with the webapp by following links. ::

    click_link("id-of-link")
    click_link("Link Text")
    click_button("Save")
    click_on("Link Text")  # clicks on either links or buttons
    click_on("Button Value")

_`Interacting with forms`
-------------------------

*Full reference:* :class:`capybara.node.actions.ActionsMixin`

There are a number of tools for interacting with form elements::

    fill_in("First Name", value="John")
    fill_in("Password", value="Seekrit")
    fill_in("Description", value="Really Long Text...")
    choose("A Radio Button")
    check("A Checkbox")
    uncheck("A Checkbox")
    attach_file("Image", "/path/to/image.jpg")
    select("Option", field="Select Box")

_`Querying`
-----------

*Full reference:* :class:`capybara.node.matchers.MatchersMixin`

Capybara has a rich set of options for querying the page for the existence of certain elements, and
working with and manipulating those elements. ::

    page.has_selector("table tr")
    page.has_selector("xpath", "//table/tr")

    page.has_xpath("//table/tr")
    page.has_css("table tr.foo")
    page.has_text("foo")

_`Finding`
----------

*Full reference:* :class:`capybara.node.finders.FindersMixin`

You can also find specific elements, in order to manipulate them::

    find_field("First Name").value
    find_button("Send").click()

    find("xpath", "//table/tr").click()
    find("#overlay").find("h1").click()

**Note**: :meth:`find <capybara.node.finders.FindersMixin.find>` will wait for an element to appear
on the page, as explained in the Ajax section. If the element does not appear it will raise an
error.

These elements all have all the Capybara DSL methods available, so you can restrict them
to specific parts of the page::

    find("#navigation").click_link("Home")

_`Scoping`
----------

Capybara makes it possible to restrict certain actions, such as clicking links, to
within a specific area of the page. For this purpose you can use the generic
:meth:`scope <capybara.session.Session.scope>` context manager. Optionally you can specify which
kind of selector to use. ::

    with scope("li#employee"):
        click_link("Jimmy")

    with scope("xpath", "//li[@id='employee']"):
        click_link("Jimmy")

_`Working with windows`
-----------------------

Capybara provides some methods to ease finding and switching windows::

    facebook_window = window_opened_by(
        lambda: click_button("Like"))
    with window(facebook_window):
        find("#login_email").set("a@example.com")
        find("#login_password").set("qwerty")
        click_button("Submit")

_`Scripting`
------------

In drivers which support it, you can easily execute JavaScript::

    page.execute_script("$('body').empty()")

For simple expressions, you can return the result of the script. Note that this may break with
more complicated expressions::

    result = page.evaluate_script("4 + 4")

_`Modals`
---------

In drivers which support it, you can accept, dismiss and respond to alerts, confirms and prompts.

You can accept or dismiss alert messages by wrapping the code that produces the alert in a context manager::

    with accept_alert():
        click_link("Show Alert")

You can accept or dismiss a confirmation by wrapping it in a context manager, as well::

    with dismiss_confirm():
        click_link("Show Confirm")

You can accept or dismiss prompts as well, and also provide text to fill in for the response::

    with accept_prompt(response="Linus Torvalds"):
        click_link("Show Prompt About Linux")

_`Debugging`
------------

It can be useful to take a snapshot of the page as it currently is and take a
look at it::

    save_page("output.html")

You can also retrieve the current state of the DOM as a string using
:attr:`page.html <capybara.session.Session.html>`. ::

    print(page.html)

This is mostly useful for debugging. You should avoid testing against the contents of
:attr:`page.html <capybara.session.Session.html>` and use the more expressive finder methods
instead.

Finally, in drivers that support it, you can save a screenshot::

    save_screenshot("screenshot.png")

_`Matching`
~~~~~~~~~~~

It is possible to customize how Capybara finds elements. At your disposal are
two options, :data:`capybara.exact` and :data:`capybara.match`.

_`Exactness`
------------

:data:`capybara.exact` and the ``exact`` option work together with the ``is_``
expression inside the XPath package. When ``exact`` is true, all ``is_``
expressions match exactly; when it is false, they allow substring matches.
Many of the selectors built into Capybara use the ``is_`` expression. This
way you can specify whether you want to allow substring matches or not.
:data:`capybara.exact` is false by default.

For example::

    click_link("Password")  # also matches "Password confirmation"
    capybara.exact = True
    click_link("Password")  # does not match "Password confirmation"
    click_link("Password", exact=False)  # can be overridden

_`Strategy`
-----------

Using :data:`capybara.match` and the equivalent ``match`` option, you can control
how Capybara behaves when multiple elements all match a query. There are
currently four different strategies built into Capybara:

1. **first:** Just picks the first element that matches.
2. **one:** Raises an error if more than one element matches.
3. **smart:** If ``exact`` is ``True``, raises an error if more than one element
   matches, just like ``one``. If ``exact`` is ``False``, it will first try to
   find an exact match. An error is raised if more than one element is found. If
   no element is found, a new search is performed which allows partial matches.
   If that search returns multiple matches, an error is raised.
4. **prefer_exact:** If multiple matches are found, some of which are exact, and
   some of which are not, then the first exactly matching element is returned.

The default for :data:`capybara.match` is ``"smart"``.

_`Asynchronous JavaScript (Ajax and friends)`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When working with asynchronous JavaScript, you might come across situations
where you are attempting to interact with an element which is not yet present
on the page. Capybara automatically deals with this by waiting for elements
to appear on the page.

When issuing instructions to the DSL such as::

    click_link("foo")
    click_link("bar")
    assert page.has_text("baz")

If clicking on the *foo* link triggers an asynchronous process, such as
an Ajax request, which, when complete will add the *bar* link to the page,
clicking on the *bar* link would be expected to fail, since that link doesn't
exist yet. However Capybara is smart enough to retry finding the link for a
brief period of time before giving up and throwing an error. The same is true of
the next line, which looks for the content *baz* on the page; it will retry
looking for that content for a brief time. You can adjust how long this period
is (the default is 2 seconds)::

    import capybara

    capybara.default_max_wait_time = 5

Be aware that because of this behavior, the follow two statements are **not**
equivalent, and you should **always** use the latter! ::

    not page.has_xpath("a")
    page.has_no_xpath("a")

The former would immediately fail because the content has not yet been removed.
Only the latter would wait for the asynchronous process to remove the content
from the page.

Capybara's waiting behavior is quite advanced, and can deal with situations
such as the following line of code::

    assert find("#sidebar").find("h1").has_text("Something")

Even if JavaScript causes ``#sidebar`` to disappear off the page, Capybara
will automatically reload it and any elements it contains. So if an AJAX
request causes the contents of ``#sidebar`` to change, which would update
the text of the ``h1`` to "Something", and this happened, this test would
pass. If you do not want this behavior, you can set
:data:`capybara.automatic_reload` to ``False``.

_`Using sessions`
~~~~~~~~~~~~~~~~~

Capybara manages named sessions ("default" if not specified) allowing multiple
sessions using the same driver and test app instance to be interacted with. A
new session will be created using the current driver if a session with the given
name using the current driver and test app instance is not found.

_`Named sessions`
-----------------

To perform operations in a different session and then revert to the previous
session::

    import capybara

    with capybara.using_session("Bob's session"):
         # do something in Bob's browser session
    # reverts to previous session

To permanently switch the current session to a different session::

    import capybara

    capybara.session_name = "some other session"

_`Using sessions manually`
--------------------------

For ultimate control, you can instantiate and use a :class:`Session <capybara.session.Session>`
manually. ::

    from capybara.session import Session

    session = Session("selenium", my_wsgi_app)
    with session.scope("//form[@id='session']"):
        session.fill_in("Email", value="email@example.com")
        session.fill_in("Password", value="password")
    session.click_button("Sign in")

_`Using the DSL elsewhere`
~~~~~~~~~~~~~~~~~~~~~~~~~~

You can access the :data:`page <capybara.dsl.page>` session proxy from anywhere by importing it::

    from capybara.dsl import page

    # ...

    with page.scope("//form[@id='session']"):
        page.fill_in("Email", value="user@example.com")
        page.fill_in("Password", value="password")
    page.click_button("Sign in")

You can mix the DSL methods into any class by inheriting from
:class:`DSLMixin <capybara.dsl.DSLMixin>`::

    from capybara.dsl import DSLMixin

    class MyClass(DSLMixin):
        def login(self):
            with self.scope("//form[@id='session']"):
                self.fill_in("Email", value="user@example.com")
                self.fill_in("Password", value="password")
            self.click_button("Sign in")

You can also mix the DSL methods into any module by importing all of :mod:`capybara.dsl`::

    from capybara.dsl import *

    def main():
        with scope("//form[@id='session']"):
            fill_in("Email", value="user@example.com")
            fill_in("Password", value="password")
        click_button("Sign in")

    if __name__ == "__main__":
        main()

This enables its use in unsupported testing frameworks, and for general-purpose
scripting.

_`Calling remote servers`
~~~~~~~~~~~~~~~~~~~~~~~~~

Normally Capybara expects to be testing an in-process WSGI application, but you
can also use it to talk to a web server running anywhere on the internet, by
setting :data:`capybara.app_host`::

    capybara.app_host = "http://www.google.com"
    # ...
    visit("/")

With drivers that support it, you can also visit any URL directly::

    visit("http://www.google.com")

_`XPath, CSS and selectors`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Capybara does not try to guess what kind of selector you are going to give it,
and will always use CSS by default. If you want to use XPath, you'll need to
do::

    with scope("xpath", "//ul/li"):
        # ...
    find("xpath", "//ul/li").text

Alternatively you can set the default selector to XPath::

    import capybara

    capybara.default_selector = "xpath"

    find("//ul/li").text

Capybara allows you to add custom selectors, which can be very useful if you
find yourself using the same kinds of selectors very often::

    from capybara.selector import add_selector
    from xpath import dsl as x

    with add_selector("id") as s:
        s.xpath = lambda id: x.descendant[x.attr("id") == str(id)]

    with add_selector("row") as s:
        s.xpath = lambda num: ".//tbody/tr[{}]".format(num)

    with add_selector("flash_type") as s:
        s.css = lambda flash_type: "#flash.{}".format(flash_type)

The block given to xpath must always return an XPath expression as a string, or
an XPath expression generated through the ``xpath-py`` package. You can now use these
selectors like this::

    find("id", "post_123")
    find("row", 3)
    find("flash_type", "notice")

_`Beware the XPath // trap`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

In XPath the expression // means something very specific, and it might not be what
you think. Contrary to common belief, // means "anywhere in the document" not "anywhere
in the current context". As an example::

    page.find("xpath", "//body").find_all("xpath", "//script")

You might expect this to find all script tags in the body, but actually, it finds all
script tags anywhere in the entire document, not only in the body! What you're looking
for is the .// expression which means "any descendant of the current node"::

    page.find("xpath", "//body").find_all("xpath", ".//script")

The same thing goes for :meth:`scope <capybara.session.Session.scope>`::

    with scope("xpath", "//body"):
        page.find("xpath", ".//script")
        with scope("xpath", ".//table/tbody"):
            # ...

_`Configuring and adding drivers`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Capybara makes it convenient to switch between different drivers. It also
exposes an API to tweak those drivers with whatever settings you want, or to
add your own drivers. This is how to override the Selenium driver
configuration to use Chrome::

    import capybara

    @capybara.register_driver("selenium")
    def init_selenium_driver(app):
        from capybara.selenium.driver import Driver

        return Driver(app, browser="chrome")

However, it's also possible to give this configuration a different name. ::

    @capybara.register_driver("selenium_chrome")
    def init_selenium_chrome_driver(app):
        from capybara.selenium.driver import Driver

        return Driver(app, browser="chrome")

Then tests can switch between using different browsers effortlessly::

    capybara.current_driver = "selenium_chrome"

Whatever is returned from the initialization function should conform to the API
described by :class:`capybara.driver.base.Base`, it does not however have to
inherit from this class.

The |selenium_wiki|_ has additional info about how the underlying driver can be
configured.

.. |selenium_wiki| replace:: Selenium wiki
.. _selenium_wiki: https://github.com/SeleniumHQ/selenium/wiki/Python-Bindings

_`Gotchas:`
~~~~~~~~~~~

* Server errors will only be raised in the session that initiates the server
  thread. If you are testing for specific server errors and using multiple
  sessions make sure to test for the errors using the initial session (usually
  ``"default"``).

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. raw:: html

   <a href="https://github.com/elliterate/capybara.py">
     <img style="position: absolute; top: 0; right: 0; border: 0;"
          src="https://camo.githubusercontent.com/a6677b08c955af8400f44c6298f40e7d19cc5b2d/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f6769746875622f726962626f6e732f666f726b6d655f72696768745f677261795f3664366436642e706e67"
          alt="Fork me on GitHub"
          data-canonical-src="https://s3.amazonaws.com/github/ribbons/forkme_right_gray_6d6d6d.png" />
   </a>
