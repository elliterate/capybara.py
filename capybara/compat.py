import sys

PY2 = sys.version_info[0] == 2

if PY2:
    from urllib import quote, unquote, urlencode
    from urllib2 import URLError, urlopen
    from urlparse import ParseResult, urlparse, parse_qsl

    bytes_ = unicode
    bytes_decode = unicode.encode
    str_encode = str.decode

    def decode_socket_data(data):
        return data

    def encode_socket_data(data):
        return data
else:
    from urllib.error import URLError
    from urllib.request import urlopen
    from urllib.parse import ParseResult, urlparse, parse_qsl, quote, unquote, urlencode

    bytes_ = bytes
    bytes_decode = bytes.decode
    str_encode = str.encode

    def decode_socket_data(data):
        return data.decode()

    def encode_socket_data(data):
        return data.encode()
