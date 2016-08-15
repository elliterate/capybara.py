Capybara
========

Capybara helps you test web applications by simulating how a real user would
interact with your app. It is agnostic about the driver running your tests and
comes with Selenium support built in.

_`Key benefits`
~~~~~~~~~~~~~~~

- **No setup** necessary for WSGI-compliant applications. Works out of the box.
- **Intuitive API** which mimics the language an actual user would use.
- **Powerful synchronization** features mean you never have to manually wait
  for asynchronous processes to complete.

_`Setup`
~~~~~~~~

To install, add ``capybara-py`` to your application's test requirements.

In your test setup, set :data:`capybara.app` to your WSGI-compliant app::

    import app
    import capybara

    capybara.app = app

_`Drivers`
~~~~~~~~~~

Capybara uses the same DSL to drive a variety of browser and headless drivers.
By default, Capybara uses the ``"selenium"`` driver.

_`Selenium`
-----------

At the moment, Capybara supports |selenium_2.0_webdriver|_, *not* Selenium RC.
In order to use Selenium, you'll need to install the ``selenium-webdriver``
package. Provided Firefox is installed, everything is set up for you, and you
should be able to start using Selenium right away.

.. |selenium_2.0_webdriver| replace:: Selenium 2.0 (Webdriver)
.. _selenium_2.0_webdriver: http://seleniumhq.org/docs/01_introducing_selenium.html#selenium-2-aka-selenium-webdriver

_`Using Capybara`
~~~~~~~~~~~~~~~~~

You can access the DSL by importing ``capybara`` and getting the
:func:`current_session <capybara.current_session>`:

    import capybara

    session = capybara.current_session()
    session.visit("/")

_`The DSL`
~~~~~~~~~~

_`Navigating`
-------------

You can use the :meth:`visit <capybara.session.Session.visit>` method to navigate to other pages::

    session.visit("/projects")

The visit method only takes a single parameter, the request method is **always**
GET.

_`Clicking links and buttons`
-----------------------------

*Full reference:* :class:`capybara.node.actions.ActionsMixin`

You can interact with the webapp by following links. ::

    session.click_link("id-of-link")
    session.click_link("Link Text")
    session.click_button("Save")
    session.click_on("Link Text")  # clicks on either links or buttons
    session.click_on("Button Value")

_`Interacting with forms`
-------------------------

*Full reference:* :class:`capybara.node.actions.ActionsMixin`

There are a number of tools for interacting with form elements::

    session.fill_in("First Name", value="John")
    session.fill_in("Password", value="Seekrit")
    session.fill_in("Description", value="Really Long Text...")
    session.choose("A Radio Button")
    session.check("A Checkbox")
    session.uncheck("A Checkbox")
    session.select("Option", field="Select Box")

_`Querying`
-----------

*Full reference:* :class:`capybara.node.matchers.MatchersMixin`

Capybara has a rich set of options for querying the page for the existence of certain elements, and
working with and manipulating those elements. ::

    session.has_selector("table tr")
    session.has_selector("xpath", "//table/tr")

    session.has_xpath("//table/tr")
    session.has_css("table tr.foo")
    session.has_text("foo")

_`Finding`
----------

*Full reference:* :class:`capybara.node.finders.FindersMixin`

You can also find specific elements, in order to manipulate them::

    session.find_field("First Name").value
    session.find_button("Send").click()

    session.find("xpath", "//table/tr").click()
    session.find("#overlay").find("h1").click()

**Note**: :meth:`find <capybara.node.finders.FindersMixin.find>` will wait for an element to appear
on the page, as explained in the Ajax section. If the element does not appear it will raise an
error.

These elements all have all the Capybara DSL methods available, so you can restrict them
to specific parts of the page::

    session.find("#navigation").click_link("Home")

_`Scoping`
----------

Capybara makes it possible to restrict certain actions, such as clicking links, to
within a specific area of the page. For this purpose you can use the generic
:meth:`scope <capybara.session.Session.scope>` context manager. Optionally you can specify which
kind of selector to use. ::

    with session.scope("li#employee"):
        session.click_link("Jimmy")

    with session.scope("xpath", "//li[@id='employee']"):
        session.click_link("Jimmy")

_`Working with windows`
-----------------------

Capybara provides some methods to ease finding and switching windows::

    facebook_window = session.window_opened_by(
        lambda: session.click_button("Like"))
    with session.window(facebook_window):
        session.find("#login_email").set("a@example.com")
        session.find("#login_password").set("qwerty")
        session.click_button("Submit")

_`Scripting`
------------

In drivers which support it, you can easily execute JavaScript::

    session.execute_script("$('body').empty()")

For simple expressions, you can return the result of the script. Note that this may break with
more complicated expressions::

    result = session.evaluate_script("4 + 4")

_`Modals`
---------

In drivers which support it, you can accept, dismiss and respond to alerts, confirms and prompts.

You can accept or dismiss alert messages by wrapping the code that produces the alert in a context manager::

    with session.accept_alert():
        session.click_link("Show Alert")

You can accept or dismiss a confirmation by wrapping it in a context manager, as well::

    with session.dismiss_confirm():
        session.click_link("Show Confirm")

You can accept or dismiss prompts as well, and also provide text to fill in for the response::

    with session.accept_prompt(response="Linus Torvalds"):
        session.click_link("Show Prompt About Linux")

_`Debugging`
------------

You can retrieve the current state of the DOM as a string using
:attr:`session.html <capybara.session.Session.html>`. ::

    print(session.html)

This is mostly useful for debugging. You should avoid testing against the contents of
:attr:`session.html <capybara.session.Session.html>` and use the more expressive finder methods
instead.

_`Asynchronous JavaScript (Ajax and friends)`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When working with asynchronous JavaScript, you might come across situations
where you are attempting to interact with an element which is not yet present
on the page. Capybara automatically deals with this by waiting for elements
to appear on the page.

When issuing instructions to the DSL such as::

    session.click_link("foo")
    session.click_link("bar")
    assert session.has_text("baz")

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

_`Calling remote servers`
~~~~~~~~~~~~~~~~~~~~~~~~~

Normally Capybara expects to be testing an in-process WSGI application, but you
can also use it to talk to a web server running anywhere on the internet, by
setting :data:`capybara.app_host`::

    capybara.app_host = "http://www.google.com"
    # ...
    session.visit("/")

With drivers that support it, you can also visit any URL directly::

    session.visit("http://www.google.com")

_`XPath, CSS and selectors`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Capybara does not try to guess what kind of selector you are going to give it,
and will always use CSS by default. If you want to use XPath, you'll need to
do::

    with session.scope("xpath", "//ul/li"):
        # ...
    session.find("xpath", "//ul/li").text

Alternatively you can set the default selector to XPath::

    import capybara

    capybara.default_selector = "xpath"

    session.find("//ul/li").text

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

    session.find("id", "post_123")
    session.find("row", 3)
    session.find("flash_type", "notice")

_`Beware the XPath // trap`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

In XPath the expression // means something very specific, and it might not be what
you think. Contrary to common belief, // means "anywhere in the document" not "anywhere
in the current context". As an example::

    session.find("xpath", "//body").find("xpath", "//script")

You might expect this to find a script tag in the body, but actually, it finds a
script tag anywhere in the entire document, not only in the body! What you're looking
for is the .// expression which means "any descendant of the current node"::

    session.find("xpath", "//body").find("xpath", ".//script")

The same thing goes for :meth:`scope <capybara.session.Session.scope>`::

    with session.scope("xpath", "//body"):
        session.find("xpath", ".//script")
        with session.scope("xpath", ".//table/tbody"):
            # ...

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
