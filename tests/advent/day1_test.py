import pytest

from tests.advent.conftest import Base


class TestDay1(Base):
    DAY = 1
    DATA = (68775, 202585)

    @pytest.fixture(params=range(len(DATA)))
    def test_cases(self, request):
        return self._create_case(request)
