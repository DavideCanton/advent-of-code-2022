from __future__ import annotations

import operator
import re
from abc import ABCMeta, abstractmethod
from collections import Counter, deque
from dataclasses import dataclass
from typing import Callable, Generic, Literal, Sequence, TextIO, TypeVar

from advent.common import SameComputationAdventDay

Num = TypeVar("Num")


def _parse(val):
    try:
        val = int(val)
    except ValueError:
        pass
    return val


@dataclass
class Monkey(Generic[Num], metaclass=ABCMeta):
    id: int
    items: deque[Num]
    test_den: int
    if_true: int
    if_false: int
    op1: int | Literal["old"]
    op2: int | Literal["old"]

    def do_turn(self, c: Counter, monkeys: dict[int, Monkey]):
        while self.items:
            c[self.id] += 1
            old = self.items.popleft()
            new, div = self._process(old)
            if div:
                dest = self.if_true
            else:
                dest = self.if_false

            monkeys[dest].items.append(new)

    @abstractmethod
    def _process(self, n: Num) -> tuple[Num, bool]:
        pass


@dataclass
class MonkeyInt(Monkey[int]):
    den: int
    op: Callable[[int, int], int]

    @classmethod
    def parse(cls, group_dict: dict, den: int) -> MonkeyInt:
        items_str: list[str] = [
            element
            for element in group_dict["items"].replace(" ", "").split(",")
            if element
        ]
        items = deque(item for item in map(int, items_str))

        opd = group_dict["op"]
        if opd == "+":
            op = operator.add
        elif opd == "*":
            op = operator.mul
        else:
            raise ValueError(f"Invalid op: {opd}")

        return MonkeyInt(
            id=int(group_dict["id"]),
            items=items,
            test_den=int(group_dict["den"]),
            if_false=int(group_dict["idf"]),
            if_true=int(group_dict["idt"]),
            den=den,
            op=op,
            op1=_parse(group_dict["op1"]),
            op2=_parse(group_dict["op2"]),
        )

    def _process(self, old: int) -> tuple[int, bool]:
        op1 = old if self.op1 == "old" else self.op1
        op2 = old if self.op2 == "old" else self.op2
        new = self.op(op1, op2) // self.den
        return new, new % self.test_den == 0


Rems = dict[int, int]


@dataclass
class MonkeyRem(Monkey[Rems]):
    op: str

    @classmethod
    def parse(cls, group_dict: dict, dens: Sequence[int]) -> MonkeyRem:
        items_str: list[str] = [
            s for s in group_dict["items"].replace(" ", "").split(",") if s
        ]
        items = deque({d: item % d for d in dens} for item in map(int, items_str))

        return MonkeyRem(
            id=int(group_dict["id"]),
            items=items,
            test_den=int(group_dict["den"]),
            if_false=int(group_dict["idf"]),
            if_true=int(group_dict["idt"]),
            op1=_parse(group_dict["op1"]),
            op2=_parse(group_dict["op2"]),
            op=group_dict["op"],
        )

    def _process(self, old: Rems) -> tuple[Rems, bool]:
        match self.op:
            case "+":
                operand = self.op2 if self.op1 == "old" else self.op1
                assert isinstance(operand, int)
                for (d, v) in old.items():
                    old[d] = (v + operand) % d
            case "*":
                operand = self.op2 if self.op1 == "old" else self.op1
                for (d, v) in old.items():
                    old[d] = (v * (v if operand == "old" else operand)) % d
        return old, old[self.test_den] == 0


MONKEY_REGEX = re.compile(
    (
        r"^Monkey (?P<id>\d+):$\n"
        r"^\s+Starting items:(?P<items>[0-9, ]*)$\n"
        r"^\s+Operation: new = (?P<op1>[0-9]+|old)\s*(?P<op>[*+])\s*(?P<op2>[0-9]+|old)$\n"
        r"^\s+Test: divisible by (?P<den>\d+)$\n"
        r"^\s+If true: throw to monkey (?P<idt>\d+)$\n"
        r"^\s+If false: throw to monkey (?P<idf>\d+)$"
    ),
    re.MULTILINE,
)


@dataclass
class Day11(SameComputationAdventDay):
    day = 11

    def parse_input(self, input: TextIO) -> list[dict]:
        return [match.groupdict() for match in MONKEY_REGEX.finditer(input.read())]

    def compute(self, var, groups: list[dict]) -> int:
        if var == 1:
            rounds = 20
            monkey_list = [MonkeyInt.parse(g, 3) for g in groups]
        else:
            rounds = 10_000
            dens = [int(g["den"]) for g in groups]
            monkey_list = [MonkeyRem.parse(g, dens) for g in groups]

        monkeys: dict[int, Monkey] = {m.id: m for m in monkey_list}

        counter = Counter()
        for _ in range(rounds):
            for monkey in monkeys.values():
                monkey.do_turn(counter, monkeys)

        m1, m2 = counter.most_common(2)
        return m1[1] * m2[1]


ProblemClass = Day11
