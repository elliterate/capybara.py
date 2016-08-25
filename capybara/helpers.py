import re

from capybara.utils import decode_bytes, isbytes, isregex


def desc(value):
    """ str: A normalized representation for a user-provided value. """

    if isbytes(value):
        value = decode_bytes(value)
    if isregex(value):
        value = value.pattern

    return repr(value)


def failure_message(description):
    """
    Returns a expectation failure message for the given query description.

    Args:
        description (str): A description of the failed query.

    Returns:
        str: A message describing the failure.
    """

    return "expected to find {}".format(description)


def normalize_text(value):
    """
    Normalizes the given value to a string of text with extra whitespace removed.

    Byte sequences are decoded. ``None`` is converted to an empty string. Everything else
    is simply cast to a string.

    Args:
        value (Any): The data to normalize.

    Returns:
        str: The normalized text.
    """

    if value is None:
        return ""

    text = decode_bytes(value) if isbytes(value) else str(value)

    return normalize_whitespace(text)


def normalize_whitespace(text):
    """
    Returns the given text with outer whitespace removed and inner whitespace collapsed.

    Args:
        text (str): The text to normalize.

    Returns:
        str: The normalized text.
    """

    return re.sub(r"\s+", " ", text, flags=re.UNICODE).strip()
