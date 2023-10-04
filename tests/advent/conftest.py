from pathlib import Path
from typing import Any, ClassVar

import pytest

from advent import CLASSES

FOLDER = Path(__file__).parent.parent.parent / "inputs"


class Base:
    DAY: ClassVar[int]
    DATA: ClassVar[tuple[Any, Any]]

    def __init_subclass__(cls) -> None:
        params = [
            pytest.param((var, test_case), id=f"var-{var}")
            for var, test_case in enumerate(cls.DATA, start=1)
        ]

        # define dynamic fixture from data
        cls.test_cases = pytest.fixture(params=params)(cls._getter)  # type: ignore

    def _getter(self, request: Any):
        return request.param

    def test(self, test_cases: tuple[Any, Any]):
        variant, exp = test_cases
        day = self.DAY
        cls = CLASSES[day]
        file_path = FOLDER / f"day{day}.txt"
        res = cls(file_path).run(variant)
        assert res == exp
