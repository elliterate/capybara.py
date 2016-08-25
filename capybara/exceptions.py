class CapybaraError(Exception):
    pass


class ElementNotFound(CapybaraError):
    pass


class ModalNotFound(CapybaraError):
    pass


class ExpectationNotMet(ElementNotFound):
    pass


class FileNotFound(CapybaraError):
    pass


class UnselectNotAllowed(CapybaraError):
    pass


class ScopeError(CapybaraError):
    pass


class WindowError(CapybaraError):
    pass
