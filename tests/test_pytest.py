from tests.compat import urljoin


pytest_plugins = ["pytester"]


def test_resets_sessions_between_tests(testdir):
    file_a = testdir.maketxtfile(file_a="File A")
    file_b = testdir.maketxtfile(file_b="File B")

    file_a_url = urljoin("file:", str(file_a))
    file_b_url = urljoin("file:", str(file_b))

    testdir.makeconftest("""
        pytest_plugins = ["capybara.pytest"]
    """)
    testdir.makepyfile("""
        def test_request_a(page):
            page.assert_no_text("File B")
            page.visit({file_a})
            page.assert_text("File A")

        def test_request_b(page):
            page.assert_no_text("File A")
            page.visit({file_b})
            page.assert_text("File B")
    """.format(file_a=repr(file_a_url), file_b=repr(file_b_url)))

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
