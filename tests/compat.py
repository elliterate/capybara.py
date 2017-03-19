import sys

PY2 = sys.version_info[0] == 2

if PY2:
    from urlparse import urljoin
else:
    from urllib.parse import urljoin
