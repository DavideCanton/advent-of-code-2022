from collections import deque
from dataclasses import dataclass
from typing import TextIO

from advent.common import SameComputationAdventDay


@dataclass
class Day6(SameComputationAdventDay[str]):
    day = 6

    def parse_input(self, input: TextIO) -> str:
        return input.read()

    def compute(self, variant: int, input: str) -> int:
        if variant == 1:
            marker_len = 4
        else:
            marker_len = 14

        start = marker_len
        buf = deque(input[:marker_len])

        while start < len(input) and len(set(buf)) != marker_len:
            c = input[start]
            start += 1
            buf.popleft()
            buf.append(c)

        return start
