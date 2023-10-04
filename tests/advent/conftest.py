from pathlib import Path
from typing import Any, ClassVar

import pytest

from advent import CLASSES
from advent.common import Variant

FOLDER = Path(__file__).parent.parent.parent / "inputs"
type TestCase = tuple[Any, Any]


class Base:
    DAY: ClassVar[int]
    DATA: ClassVar[TestCase]

    @staticmethod
    def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
        cls: type[Base] = metafunc.cls  # type: ignore

        params: list[Any] = [
            pytest.param(var, test_case, id=f"var-{var}")
            for var, test_case in enumerate(cls.DATA, start=1)
        ]

        metafunc.parametrize("variant, exp", params)

    def test(self, variant: Variant, exp: Any) -> None:
        day = self.DAY
        cls = CLASSES[day]
        file_path = FOLDER / f"day{day}.txt"
        res = cls(file_path).run(variant)
        assert res == exp
