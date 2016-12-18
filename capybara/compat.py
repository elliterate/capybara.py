import sys

PY2 = sys.version_info[0] == 2

if PY2:
    from urllib2 import URLError, urlopen
    from urlparse import ParseResult, urlparse

    bytes_ = unicode
    bytes_decode_attr_name = "encode"
    string_encode_attr_name = "decode"

    def wsgi_decode_body(body):
        return body

    def wsgi_encode_body(body):
        return body
else:
    from urllib.error import URLError
    from urllib.request import urlopen
    from urllib.parse import ParseResult, urlparse

    bytes_ = bytes
    bytes_decode_attr_name = "decode"
    string_encode_attr_name = "encode"

    def wsgi_decode_body(body):
        return body.decode()

    def wsgi_encode_body(body):
        return body.encode()
