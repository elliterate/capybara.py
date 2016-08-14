class CapybaraError(Exception):
    pass


class ElementNotFound(CapybaraError):
    pass


class ExpectationNotMet(ElementNotFound):
    pass


class UnselectNotAllowed(CapybaraError):
    pass
