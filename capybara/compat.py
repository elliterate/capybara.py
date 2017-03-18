import sys

PY2 = sys.version_info[0] == 2

if PY2:
    from urllib import quote, unquote, urlencode
    from urllib2 import URLError, urlopen
    from urlparse import ParseResult, urlparse, parse_qsl

    bytes_ = unicode
    bytes_decode = unicode.encode
    str_encode = str.decode

    def wsgi_decode_body(body):
        return body

    def wsgi_encode_body(body):
        return body
else:
    from urllib.error import URLError
    from urllib.request import urlopen
    from urllib.parse import ParseResult, urlparse, parse_qsl, quote, unquote, urlencode

    bytes_ = bytes
    bytes_decode = bytes.decode
    str_encode = str.encode

    def wsgi_decode_body(body):
        return body.decode()

    def wsgi_encode_body(body):
        return body.encode()
