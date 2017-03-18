import os
import pytest
import re
import shutil

import capybara
from capybara.tests.compat import patch


@pytest.mark.requires("screenshot")
class TestSaveScreenshot:
    @pytest.fixture
    def alternative_path(self):
        return os.path.join(os.getcwd(), "save_screenshot_tmp")

    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/foo")

    @pytest.fixture(autouse=True)
    def teardown_settings_and_files(self, alternative_path):
        yield

        capybara.save_path = None

        if os.path.isdir(alternative_path):
            shutil.rmtree(alternative_path)

    def test_generates_sensible_filename(self, session):
        with patch.object(session.driver, "save_screenshot") as save_screenshot:
            session.save_screenshot()

            regex = re.compile(os.path.abspath("capybara-\d+\.png"))

            assert len(save_screenshot.call_args_list) == 1
            assert regex.search(save_screenshot.call_args[0][0])

    def test_allows_one_to_specify_another_path(self, session, alternative_path):
        with patch.object(session.driver, "save_screenshot") as save_screenshot:
            capybara.save_path = alternative_path

            custom_path = "screenshots/1.png"
            session.save_screenshot(custom_path)

            regex = re.compile(re.escape(custom_path) + "$")

            assert len(save_screenshot.call_args_list) == 1
            assert regex.search(save_screenshot.call_args[0][0])

    def test_saves_file_in_custom_save_path(self, session, alternative_path):
        with patch.object(session.driver, "save_screenshot") as save_screenshot:
            capybara.save_path = alternative_path

            session.save_screenshot()

            regex = re.compile(os.path.normpath(os.path.join(alternative_path, "capybara-\d+\.png")))

            assert len(save_screenshot.call_args_list) == 1
            assert regex.search(save_screenshot.call_args[0][0])

    def test_saves_file_relative_to_custom_save_path(self, session, alternative_path):
        with patch.object(session.driver, "save_screenshot") as save_screenshot:
            capybara.save_path = alternative_path

            custom_path = "screenshots/1.png"
            session.save_screenshot(custom_path)

            regex = re.compile(os.path.normpath(os.path.join(alternative_path, re.escape(custom_path))))

            assert len(save_screenshot.call_args_list) == 1
            assert regex.search(save_screenshot.call_args[0][0])
