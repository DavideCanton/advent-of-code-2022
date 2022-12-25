import importlib
from pathlib import Path
from typing import ClassVar

import pytest

FOLDER = Path(__file__).parent.parent.parent / "inputs"


class Base:
    DAY: ClassVar[int]
    DATA: ClassVar[tuple]

    def _create_case(self, request):
        index = request.param
        val = self.DATA[index]
        if val is None:
            pytest.skip()
        return (index + 1, val)

    def test(self, test_cases):
        variant, exp = test_cases
        module = importlib.import_module(f"advent.day{self.DAY}")
        res = module.ProblemClass(FOLDER).run(variant)
        assert res == exp
