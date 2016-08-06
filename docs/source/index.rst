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

_`Clicking links`
-----------------

*Full reference:* :class:`capybara.node.actions.ActionsMixin`

You can interact with the webapp by following links. ::

    session.click_link("id-of-link")
    session.click_link("Link Text")

_`Querying`
-----------

*Full reference:* :class:`capybara.node.matchers.MatchersMixin`

Capybara has a rich set of options for querying the page for the existence of certain elements, and
working with and manipulating those elements. ::

    session.has_selector("table tr")
    session.has_selector("xpath", "//table/tr")

    session.has_xpath("//table/tr")
    session.has_text("foo")

_`Finding`
----------

*Full reference:* :class:`capybara.node.finders.FindersMixin`

You can also find specific elements, in order to manipulate them::

    session.find("xpath", "//table/tr").text

**Note**: :meth:`find <capybara.node.finders.FindersMixin.find>` will wait for an element to appear
on the page, as explained in the Ajax section. If the element does not appear it will raise an
error.

These elements all have all the Capybara DSL methods available, so you can restrict them
to specific parts of the page::

    session.find("xpath", ".//*[@id='navigation']").click_link("Home")

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
