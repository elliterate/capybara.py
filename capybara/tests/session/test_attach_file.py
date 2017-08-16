import os.path
import pytest

from capybara.exceptions import ElementNotFound, FileNotFound

from capybara.tests.helpers import extract_results


class AttachFileTestCase:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/form")

    @pytest.fixture
    def file_path(self, fixture_path):
        return fixture_path("file.txt")

    @pytest.fixture
    def another_file_path(self, fixture_path):
        return fixture_path("another_file.txt")

    @pytest.fixture
    def jpg_file_path(self, fixture_path):
        return fixture_path("capybara.jpg")


class TestAttachFile(AttachFileTestCase):
    def test_raises_an_error_with_a_locator_that_does_not_exist(self, session, file_path):
        with pytest.raises(ElementNotFound) as excinfo:
            session.attach_file("does not exist", file_path)
        assert "Unable to find file field 'does not exist'" in str(excinfo.value)

    def test_raises_an_error_with_a_path_that_does_not_exist(self, session):
        with pytest.raises(FileNotFound):
            session.attach_file("Image", "/no_such_file.png")

    def test_sets_a_file_path_by_partial_label(self, session, file_path):
        session.attach_file("Imag", file_path)
        session.click_button("awesome")
        assert extract_results(session)["form[image]"] == os.path.basename(file_path)

    def test_does_not_set_a_file_path_by_partial_label_when_exact_is_true(self, session, file_path):
        with pytest.raises(ElementNotFound):
            session.attach_file("Imag", file_path, exact=True)


class TestAttachFileWithNormalForm(AttachFileTestCase):
    def test_sets_a_file_path_by_id(self, session, file_path):
        session.attach_file("form_image", file_path)
        session.click_button("awesome")
        assert extract_results(session)["form[image]"] == os.path.basename(file_path)

    def test_sets_a_file_path_by_label(self, session, file_path):
        session.attach_file("Image", file_path)
        session.click_button("awesome")
        assert extract_results(session)["form[image]"] == os.path.basename(file_path)


class TestAttachFileWithMultipartForm(AttachFileTestCase):
    def test_sets_a_file_path_by_id(self, session, file_path):
        session.attach_file("form_document", file_path)
        session.click_button("Upload Single")
        assert session.has_text(open(file_path).read())

    def test_sets_a_file_path_by_label(self, session, file_path):
        session.attach_file("Single Document", file_path)
        session.click_button("Upload Single")
        assert session.has_text(open(file_path).read())

    def test_does_not_break_if_no_file_is_submitted(self, session):
        session.click_button("Upload Single")
        assert session.has_text("No file uploaded")

    def test_sends_content_type_text_plain_when_uploading_a_text_file(self, session, file_path):
        session.attach_file("Single Document", file_path)
        session.click_button("Upload Single")
        assert session.has_text("text/plain")

    def test_sends_content_type_image_jpeg_when_uploading_an_image(self, session, jpg_file_path):
        session.attach_file("Single Document", jpg_file_path)
        session.click_button("Upload Single")
        assert session.has_text("image/jpeg")

    def test_does_not_break_when_using_html5_multiple_file_input(self, session, file_path):
        session.attach_file("Multiple Documents", file_path)
        session.click_button("Upload Multiple")
        assert session.has_text(open(file_path).read())

    def test_does_not_send_anything_when_attaching_no_files_to_a_multiple_upload_field(self, session):
        session.click_button("Upload Empty Multiple")
        assert session.has_text("Successfully ignored empty file field")
