import pytest
import sys
if sys.version_info >= (3, 3):
    from unittest.mock import NonCallableMock
else:
    from mock import NonCallableMock

from capybara.result import Result


class TestResult:
    @pytest.fixture
    def children(self):
        return [
            NonCallableMock(),
            NonCallableMock(),
            NonCallableMock(),
            NonCallableMock()]

    @pytest.fixture
    def query(self):
        return NonCallableMock(**{'matches_filters.return_value': True})

    @pytest.fixture
    def result(self, children, query):
        return Result(children, query)

    def test_has_a_length(self, result):
        assert len(result) == 4

    def test_returns_an_element_by_its_index(self, result, children):
        assert result[0] == children[0]
        assert result[1] == children[1]
        assert result[2] == children[2]
        assert result[3] == children[3]
