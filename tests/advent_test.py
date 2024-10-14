from pathlib import Path
from typing import Any, ClassVar

import pytest

from advent import get_handler_for_day
from advent.common import Variant

FOLDER = Path(__file__).parent.parent / "inputs"
type TestCase = tuple[Any, Any]


class Base:
    DAY: ClassVar[int]
    DATA: ClassVar[TestCase]
    SKIP_VARIANT: tuple[Variant, ...] = ()

    @staticmethod
    def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
        cls: type[Base] = metafunc.cls  # type: ignore

        params: list[Any] = [
            pytest.param(var, test_case, id=f"var-{var}")
            for var, test_case in enumerate(cls.DATA, start=1)
        ]

        metafunc.parametrize("variant, exp", params)

    def test(self, variant: Variant, exp: Any) -> None:
        if variant in self.SKIP_VARIANT:
            pytest.skip(reason=f"Skipping {self.__class__.__name__}, variant {variant}")

        day = self.DAY
        cls = get_handler_for_day(day)
        file_path = FOLDER / f"day{day}.txt"
        with file_path.open() as f:
            res = cls(f).run(variant)
        assert res == exp


class TestDay1(Base):
    DAY = 1
    DATA = (68775, 202585)


class TestDay2(Base):
    DAY = 2
    DATA = (14264, 12382)


class TestDay3(Base):
    DAY = 3
    DATA = (7691, 2508)


class TestDay4(Base):
    DAY = 4
    DATA = (487, 849)


class TestDay5(Base):
    DAY = 5
    DATA = ("SHMSDGZVC", "VRZGHDFBQ")


class TestDay6(Base):
    DAY = 6
    DATA = (1198, 3120)


class TestDay7(Base):
    DAY = 7
    DATA = (1886043, 3842121)


class TestDay8(Base):
    DAY = 8
    DATA = (1679, 536625)


class TestDay9(Base):
    DAY = 9
    DATA = (6269, 2557)


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


class TestDay11(Base):
    DAY = 11
    DATA = (99852, 25935263541)


class TestDay12(Base):
    DAY = 12
    DATA = (517, 512)


class TestDay13(Base):
    DAY = 13
    DATA = (4643, 21614)


class TestDay14(Base):
    DAY = 14
    DATA = (805, 25161)


class TestDay15(Base):
    DAY = 15
    DATA = (5461729, 10621647166538)


class TestDay16(Base):
    DAY = 16
    DATA = (1647, 2169)


class TestDay17(Base):
    DAY = 17
    DATA = (3188, 1591977077342)


class TestDay18(Base):
    DAY = 18
    DATA = (3494, 2062)
