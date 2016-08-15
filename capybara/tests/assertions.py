from capybara.exceptions import CapybaraError


def assert_windows_open(session, count):
    @session.document.synchronize(wait=2, errors=(CapybaraError,))
    def assert_windows_open():
        if len(session.windows) != count:
            raise CapybaraError()
    assert_windows_open()
