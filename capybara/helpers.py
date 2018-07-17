import re
import time

from capybara.compat import PY2, str_
from capybara.utils import decode_bytes, isbytes, isregex, isstring, encode_string


def declension(singular, plural, count):
    """
    Returns the appropriate word variation for the given quantity.

    Args:
        singular (str): The singular variation.
        plural (str): The plural variation.
        count (int): The count.

    Returns:
        str: The appropriate variation for the quantity.
    """

    return singular if count == 1 else plural


def desc(value):
    """ str: A normalized representation for a user-provided value. """

    def normalize_strings(value):
        if isinstance(value, list):
            value = [normalize_strings(e) for e in value]

        if isinstance(value, dict):
            value = {normalize_strings(k): normalize_strings(v) for k, v in iter(value.items())}

        if isregex(value):
            value = value.pattern

        if isbytes(value):
            value = decode_bytes(value)

        if PY2:
            if isstring(value):
                # In Python 2, strings (``unicode`` objects) represent as ``u'...'``, so ensure
                # the string is encoded (as a ``str`` object) for cleaner representation.
                value = encode_string(value)

        return value

    value = normalize_strings(value)

    return repr(value)


def expects_none(options):
    """
    Returns whether the given query options expect a possible count of zero.

    Args:
        options (Dict[str, int | Iterable[int]]): A dictionary of query options.

    Returns:
        bool: Whether a possible count of zero is expected.
    """

    if any(options.get(key) is not None for key in ["count", "maximum", "minimum", "between"]):
        return matches_count(0, options)
    else:
        return False


def failure_message(description, options):
    """
    Returns a expectation failure message for the given query description.

    Args:
        description (str): A description of the failed query.
        options (Dict[str, Any]): The query options.

    Returns:
        str: A message describing the failure.
    """

    message = "expected to find {}".format(description)

    if options["count"] is not None:
        message += " {count} {times}".format(
            count=options["count"],
            times=declension("time", "times", options["count"]))
    elif options["between"] is not None:
        between = options["between"]
        if between:
            first, last = between[0], between[-1]
        else:
            first, last = None, None

        message += " between {first} and {last} times".format(
            first=first,
            last=last)
    elif options["maximum"] is not None:
        message += " at most {maximum} {times}".format(
            maximum=options["maximum"],
            times=declension("time", "times", options["maximum"]))
    elif options["minimum"] is not None:
        message += " at least {minimum} {times}".format(
            minimum=options["minimum"],
            times=declension("time", "times", options["minimum"]))

    return message


def matches_count(count, options):
    """
    Returns whether the given count matches the given query options.

    If no quantity options are specified, any count is considered acceptable.

    Args:
        count (int): The count to be validated.
        options (Dict[str, int | Iterable[int]]): A dictionary of query options.

    Returns:
        bool: Whether the count matches the options.
    """

    if options.get("count") is not None:
        return count == int(options["count"])
    if options.get("maximum") is not None and int(options["maximum"]) < count:
        return False
    if options.get("minimum") is not None and int(options["minimum"]) > count:
        return False
    if options.get("between") is not None and count not in options["between"]:
        return False
    return True


def monotonic():
    """ float: Returns the current time, using a monotonic clock where available. """
    if hasattr(time, "monotonic"):
        return time.monotonic()
    else:
        return time.time()


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

    text = decode_bytes(value) if isbytes(value) else str_(value)

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


class Timer:
    """
    Args:
        expire_in (int): The number of seconds from now in which this timer should expire.
    """

    def __init__(self, expire_in):
        self._start = monotonic()
        self._expire_in = expire_in

    @property
    def expired(self):
        """ bool: Whether this timer has expired. """
        return monotonic() - self._start >= self._expire_in

    @property
    def stalled(self):
        """ bool: Whether this timer appears to have stalled. """
        return monotonic() == self._start


def toregex(text, exact=False):
    """
    Returns a compiled regular expression for the given text.

    Args:
        text (str | RegexObject): The text to match.
        exact (bool, optional): Whether the generated regular expression should match exact
            strings. Defaults to False.

    Returns:
        RegexObject: A compiled regular expression that will match the text.
    """

    if isregex(text):
        return text

    escaped = re.escape(normalize_text(text))
    if exact:
        escaped = r"\A{}\Z".format(escaped)

    return re.compile(escaped)
