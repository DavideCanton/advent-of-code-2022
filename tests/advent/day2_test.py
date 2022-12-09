import pytest

from tests.advent.conftest import Base


class TestDay2(Base):
    @pytest.fixture(params=list(enumerate((14264, 12382))))
    def data(self, request):
        index, res = request.param
        return (2, index + 1, res)
