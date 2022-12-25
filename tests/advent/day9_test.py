import pytest

from tests.advent.conftest import Base


class TestDay9(Base):
    DAY = 9
    DATA = (6269, 2557)

    @pytest.fixture(params=range(len(DATA)))
    def test_cases(self, request):
        return self._create_case(request)
