from capybara.utils import decode_bytes, isbytes


def desc(value):
    """ str: A normalized representation for a user-provided value. """

    if isbytes(value):
        value = decode_bytes(value)

    return repr(value)


def normalize_text(value):
    """
    Normalizes the given value to a string of text.

    Byte sequences are decoded. ``None`` is converted to an empty string. Everything else
    is simply cast to a string.

    Args:
        value (Any): The data to normalize.

    Returns:
        str: The normalized text.
    """

    if value is None:
        return ""

    return decode_bytes(value) if isbytes(value) else str(value)
