from collections import deque
from dataclasses import dataclass
from typing import TextIO, override

from advent.common import SameComputationAdventDay, Variant


@dataclass
class Day6(SameComputationAdventDay[str]):
    @override
    def parse_input(self, input: TextIO) -> str:
        return input.read()

    @override
    def compute(self, var: Variant, input: str) -> int:
        if var == 1:
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
