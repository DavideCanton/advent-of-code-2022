import pytest

from tests.advent.conftest import Base


class TestDay10(Base):
    DAY = 10
    DATA = (
        14420,
        (
            "###...##..#....###..###..####..##..#..#.\n"
            "#..#.#..#.#....#..#.#..#....#.#..#.#..#.\n"
            "#..#.#....#....#..#.###....#..#..#.#..#.\n"
            "###..#.##.#....###..#..#..#...####.#..#.\n"
            "#.#..#..#.#....#.#..#..#.#....#..#.#..#.\n"
            "#..#..###.####.#..#.###..####.#..#..##.."
        ),
    )

    @pytest.fixture(params=range(len(DATA)))
    def test_cases(self, request):
        return self._create_case(request)
