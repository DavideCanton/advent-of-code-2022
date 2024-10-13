from __future__ import annotations

from dataclasses import dataclass
from functools import total_ordering
from itertools import chain
from typing import override

from advent.common import BaseAdventDay

type PacketElement = int | list["PacketElement"]


@dataclass(order=False, eq=True)
@total_ordering
class Packet:
    elements: list[PacketElement]

    @classmethod
    def from_line(cls, line: str) -> Packet:
        return cls(eval(line, {}))

    def __lt__(self, other: Packet) -> bool:
        res = self._compare(self.elements, other.elements)
        if res is None:
            return True
        return res

    def _compare(self, p1: PacketElement, p2: PacketElement) -> bool | None:
        int1 = isinstance(p1, int)
        int2 = isinstance(p2, int)

        if int1 and int2:
            return self._cmp_int(p1, p2)

        if int1:
            p1 = [p1]
        if int2:
            p2 = [p2]

        assert isinstance(p1, list) and isinstance(p2, list)

        for e1, e2 in zip(p1, p2):
            res = self._compare(e1, e2)
            if res is not None:
                return res

        return self._cmp_int(len(p1), len(p2))

    def _cmp_int(self, n1: int, n2: int) -> bool | None:
        if n1 == n2:
            return None
        return n1 < n2


Input = list[tuple[Packet, Packet]]


@dataclass
class Day13(BaseAdventDay[Input]):
    @override
    def parse_input(self) -> Input:
        lists: list[Packet] = []
        output: Input = []
        for line in self.input:
            line = line.strip()
            if not line:
                continue
            lists.append(Packet.from_line(line))
            if len(lists) == 2:
                output.append(tuple(lists))  # type: ignore
                lists.clear()

        return output

    @override
    def _run_1(self, input: Input):
        return sum(i for i, (p1, p2) in enumerate(input, start=1) if p1 < p2)

    @override
    def _run_2(self, input: Input):
        div1 = Packet([[2]])
        div2 = Packet([[6]])
        all_packets = sorted(chain.from_iterable(input + [(div1, div2)]))
        ind1 = all_packets.index(div1) + 1
        ind2 = all_packets.index(div2) + 1
        return ind1 * ind2
