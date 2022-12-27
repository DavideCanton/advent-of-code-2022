from dataclasses import dataclass
from typing import TextIO

from advent.common import BaseAdventDay


@dataclass
class Day1(BaseAdventDay[list[int]]):
    day = 1

    def parse_input(self, input: TextIO) -> list[int]:
        calories = [0]
        for line in input:
            line = line.strip()
            if line:
                calories[-1] += int(line)
            else:
                calories.append(0)
        return calories

    def _run_1(self, calories: list[int]):
        return max(calories)

    def _run_2(self, calories: list[int]):
        return sum(sorted(calories, reverse=True)[:3])
