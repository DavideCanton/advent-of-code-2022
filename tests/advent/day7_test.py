import pytest

from tests.advent.conftest import Base


class TestDay7(Base):
    DAY = 7
    DATA = (1886043, 3842121)

    @pytest.fixture(params=range(len(DATA)))
    def test_cases(self, request):
        return self._create_case(request)
