import pytest

from tests.advent.conftest import Base


class TestDay2(Base):
    DAY = 2
    DATA = (14264, 12382)

    @pytest.fixture(params=range(len(DATA)))
    def test_cases(self, request):
        return self._create_case(request)
