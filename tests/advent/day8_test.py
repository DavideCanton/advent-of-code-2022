import pytest

from tests.advent.conftest import Base


class TestDay8(Base):
    DAY = 8
    DATA = (1679, 536625)

    @pytest.fixture(params=range(len(DATA)))
    def test_cases(self, request):
        return self._create_case(request)
