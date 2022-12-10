import pytest

from tests.advent.conftest import Base


class TestDay3(Base):
    DAY = 3
    DATA = (7691, 2508)

    @pytest.fixture(params=range(len(DATA)))
    def test_cases(self, request):
        return self._create_case(request)
