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
        setattr(  # noqa: B010
            cls,
            "test_cases",
            pytest.fixture(params=params)(lambda self, request: request.param),
        )

    def test(self, test_cases):
        variant, exp = test_cases
        cls = CLASSES[self.DAY]
        res = cls(FOLDER).run(variant)
        assert res == exp
