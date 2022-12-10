import pytest

from tests.advent.conftest import Base


class TestDay4(Base):
    DAY = 4
    DATA = (487, 849)

    @pytest.fixture(params=range(len(DATA)))
    def test_cases(self, request):
        return self._create_case(request)
