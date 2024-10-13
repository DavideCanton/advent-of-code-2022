from dataclasses import dataclass
from typing import override

from advent.common import BaseAdventDay


@dataclass
class Day1(BaseAdventDay[list[int]]):
    @override
    def parse_input(self) -> list[int]:
        calories = [0]
        for line in self.input:
            line = line.strip()
            if line:
                calories[-1] += int(line)
            else:
                calories.append(0)
        return calories

    @override
    def _run_1(self, input: list[int]) -> int:
        return max(input)

    @override
    def _run_2(self, input: list[int]) -> int:
        return sum(sorted(input, reverse=True)[:3])
