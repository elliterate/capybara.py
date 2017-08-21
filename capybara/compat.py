import sys

PY2 = sys.version_info[0] == 2

if PY2:
    from urllib import quote, unquote, urlencode
    from urllib2 import URLError, urlopen
    from urlparse import ParseResult, urlparse, parse_qsl

    bytes_ = str
    str_ = unicode
else:
    from urllib.error import URLError
    from urllib.request import urlopen
    from urllib.parse import ParseResult, urlparse, parse_qsl, quote, unquote, urlencode

    bytes_ = bytes
    str_ = str
