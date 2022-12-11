import pytest

from tests.advent.conftest import Base


class TestDay6(Base):
    DAY = 6
    DATA = (1198, 3120)

    @pytest.fixture(params=range(len(DATA)))
    def test_cases(self, request):
        return self._create_case(request)
