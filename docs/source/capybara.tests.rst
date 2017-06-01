capybara.tests package
======================

This is a test suite for verifying the implementation of a third-party driver, exposed as
`a pytest plugin`_.

.. _a pytest plugin: https://docs.pytest.org/en/latest/plugins.html

_`Using`
~~~~~~~~

To use, add the pytest plugin in your ``conftest.py``::

    pytest_plugins = ["capybara.tests.pytest_plugin"]

Then, add a test file (e.g., ``tests/test_my_custom_driver.py``) that registers your driver and
instantiates a test suite::

    import capybara
    from capybara.tests.suite import DriverSuite


    @capybara.register_driver("my_custom_driver")
    def init_my_custom_driver(app):
        from my_custom_driver.driver import Driver

        return Driver(app)


    MyCustomDriverSuite = DriverSuite(
        # The name used to register your driver.
        "my_custom_driver",

        # Features not supported by your driver.
        skip=["modals", "windows"]

Now, whenever this file is collected by a pytest session, the tests in the verification suite will
be included and run against your registered driver.

_`Including implicit test dependencies`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This test suite relies on a number of third-party dependencies that, because they are not needed
for the operation of Capybara itself, are not included in its ``requires`` configuration and thus
will *not* be automatically pulled in by your package. You will need to manually add and maintain
these dependencies in the ``tests_require`` configuration of your ``setup.py``::

    setup(
        # ...
        tests_require=["flaky", "flask", "mock", "py", "pytest >= 3", "werkzeug"])  # as of writing

Submodules
----------

capybara.tests.suite module
---------------------------

.. automodule:: capybara.tests.suite
    :members:
    :undoc-members:
    :show-inheritance:


Module contents
---------------

.. automodule:: capybara.tests
    :members:
    :undoc-members:
    :show-inheritance:
