import sys

PY2 = sys.version_info[0] == 2

if PY2:
    from mock import NonCallableMock, patch
else:
    from unittest.mock import NonCallableMock, patch
