pytest_plugins = ["pytester"]


def test_resets_sessions_between_tests(testdir):
    testdir.makepyfile(test_app="""
        from flask import Flask

        app = Flask(__name__)

        @app.route("/a")
        def a():
            return "Page A"

        @app.route("/b")
        def b():
            return "Page B"
    """)
    testdir.makeconftest("""
        import capybara
        import test_app

        pytest_plugins = ["capybara.pytest"]

        capybara.app = test_app.app
    """)
    testdir.makepyfile("""
        def test_request_a(page):
            page.assert_no_text("Page B")
            page.visit("/a")
            page.assert_text("Page A")

        def test_request_b(page):
            page.assert_no_text("Page A")
            page.visit("/b")
            page.assert_text("Page B")
    """)

    result = testdir.runpytest()
    result.assert_outcomes(passed=2)


def test_provides_a_page_fixture(testdir):
    testdir.makeconftest("""
        pytest_plugins = ["capybara.pytest"]
    """)
    testdir.makepyfile("""
        import capybara.dsl

        def test_page_fixture(page):
            assert page == capybara.dsl.page
    """)

    result = testdir.runpytest()
    result.assert_outcomes(passed=1)
