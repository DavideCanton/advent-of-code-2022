import pytest

from tests.advent.conftest import Base


class TestDay5(Base):
    DAY = 5
    DATA = ("SHMSDGZVC", "VRZGHDFBQ")

    @pytest.fixture(params=range(len(DATA)))
    def test_cases(self, request):
        return self._create_case(request)
