import pytest

from tests.advent.conftest import Base


class TestDay1(Base):
    @pytest.fixture(params=list(enumerate((68775, 202585))))
    def data(self, request):
        index, res = request.param
        return (1, index + 1, res)
