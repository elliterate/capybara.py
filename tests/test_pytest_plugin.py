import pytest


pytest_plugins = ["pytester"]


@pytest.fixture(autouse=True)
def make_test_app(testdir):
    testdir.makepyfile(test_app="""
        from flask import Flask

        app = Flask(__name__)

        @app.route("/js")
        def home():
            return \"\"\"
              <html><body>
                <script type="text/javascript">
                  document.write(
                    "Th" + "is i" + "s fo" + "r " + "Java" + "Script browsers."
                  );
                </script>
                <noscript>
                  This is for non-JavaScript browsers.
                </noscript>
              </body></html>
            \"\"\"

        @app.route("/a")
        def a():
            return "Page A"

        @app.route("/b")
        def b():
            return "Page B"
    """)


@pytest.fixture(autouse=True)
def make_conftest(testdir):
    testdir.makeconftest("""
        import capybara
        import test_app

        pytest_plugins = ["capybara.pytest_plugin"]

        capybara.app = test_app.app

        @capybara.register_driver("selenium")
        def init_selenium_driver(app):
            from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

            from capybara.selenium.driver import Driver

            capabilities = DesiredCapabilities.FIREFOX.copy()
            capabilities["marionette"] = False

            return Driver(app, browser="firefox", desired_capabilities=capabilities)
    """)


def test_switches_to_the_javascript_driver_when_marked(testdir):
    testdir.makepyfile("""
        import capybara
        import pytest

        @pytest.mark.js
        def test_uses_javascript_driver(page):
            assert capybara.current_driver == capybara.javascript_driver
            page.visit("/js")
            page.assert_text("This is for JavaScript browsers.")
            page.assert_no_text("This is for non-JavaScript browsers.")

        def test_uses_default_driver(page):
            assert capybara.current_driver is None
            page.visit("/js")
            page.assert_no_text("This is for JavaScript browsers.")
            page.assert_text("This is for non-JavaScript browsers.")
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=2)


def test_switches_to_the_specified_driver_when_marked(testdir):
    testdir.makepyfile("""
        import capybara
        import pytest

        @pytest.mark.driver("selenium")
        def test_uses_selenium_driver():
            assert capybara.current_driver == "selenium"

        @pytest.mark.driver("werkzeug")
        def test_uses_werkzeug_driver():
            assert capybara.current_driver == "werkzeug"
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=2)


def test_resets_sessions_between_tests(testdir):
    testdir.makepyfile("""
        def test_sees_only_page_a(page):
            page.assert_no_text("Page B")
            page.visit("/a")
            page.assert_text("Page A")

        def test_sees_only_page_b(page):
            page.assert_no_text("Page A")
            page.visit("/b")
            page.assert_text("Page B")
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=2)


def test_restores_the_default_driver(testdir):
    testdir.makepyfile("""
        import capybara

        def test_does_not_see_werkzeug_driver():
            assert capybara.current_driver is None
            capybara.current_driver = "selenium"
            assert capybara.current_driver == "selenium"

        def test_does_not_see_selenium_driver():
            assert capybara.current_driver is None
            capybara.current_driver = "werkzeug"
            assert capybara.current_driver == "werkzeug"
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=2)


def test_provides_a_page_fixture(testdir):
    testdir.makepyfile("""
        import capybara.dsl

        def test_page_fixture(page):
            assert page == capybara.dsl.page
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)
