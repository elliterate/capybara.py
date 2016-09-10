from glob import glob
import os
import pytest
import re
import shutil

import capybara


class TestSavePage:
    @pytest.fixture
    def alternative_path(self):
        return os.path.join(os.getcwd(), "save_page_tmp")

    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/foo")

    @pytest.fixture(autouse=True)
    def teardown_settings_and_files(self, alternative_path):
        yield

        capybara.save_path = None

        for path in glob("capybara-*.html"):
            os.remove(path)

        if os.path.isdir(alternative_path):
            shutil.rmtree(alternative_path)

    def test_saves_the_page_in_the_root_directory(self, session):
        session.save_page()
        path = glob("capybara-*.html")[0]
        assert "Another World" in open(path).read()

    def test_generates_a_sensible_filename(self, session):
        session.save_page()
        filename = glob("capybara-*.html")[0]
        assert re.compile(r"^capybara-\d+\.html$").match(filename)

    def test_can_store_files_in_a_specified_directory(self, session, alternative_path):
        capybara.save_path = alternative_path
        session.save_page()
        path = glob(os.path.join(alternative_path, "capybara-*.html"))[0]
        assert "Another World" in open(path).read()

    def test_uses_the_given_filename(self, session):
        session.save_page("capybara-001122.html")
        assert "Another World" in open("capybara-001122.html").read()

    def test_can_store_files_in_a_specified_directory_with_a_given_filename(self, session, alternative_path):
        capybara.save_path = alternative_path
        session.save_page("capybara-001133.html")
        path = os.path.join(alternative_path, "capybara-001133.html")
        assert "Another World" in open(path).read()

    def test_can_store_files_in_a_specified_directory_with_a_given_relative_filename(self, session, alternative_path):
        capybara.save_path = alternative_path
        session.save_page("tmp/capybara-001144.html")
        path = os.path.join(alternative_path, "tmp/capybara-001144.html")
        assert "Another World" in open(path).read()

    def test_returns_an_absolute_path(self, session):
        result = session.save_page()
        path = os.path.abspath(glob("capybara-*.html")[0])
        assert result == path
