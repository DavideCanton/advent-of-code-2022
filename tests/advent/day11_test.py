import pytest

from tests.advent.conftest import Base


class TestDay11(Base):
    DAY = 11
    DATA = (99852, 25935263541)

    @pytest.fixture(params=range(len(DATA)))
    def test_cases(self, request):
        return self._create_case(request)
