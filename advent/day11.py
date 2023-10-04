from __future__ import annotations

import re
from collections import Counter, deque
from dataclasses import dataclass
from math import lcm
from operator import add, mul
from typing import Callable, Literal, TextIO, TypedDict, cast, override

from advent.common import SameComputationAdventDay, Variant

type Old = Literal["old"]


@dataclass
class Monkey:
    id: int
    items: deque[int]
    test_den: int
    if_true: int
    if_false: int
    operand1: int | Old
    operand2: int | Old
    operation: Callable[[int, int], int]
    post_op: Callable[[int], int]

    def do_turn(self, counter: Counter[int], monkeys: dict[int, Monkey]):
        while self.items:
            counter[self.id] += 1
            old = self.items.popleft()
            new, div = self._process(old)
            if div:
                dest = self.if_true
            else:
                dest = self.if_false

            monkeys[dest].items.append(new)

    def _process(self, old: int) -> tuple[int, bool]:
        op1 = old if self.operand1 == "old" else self.operand1
        op2 = old if self.operand2 == "old" else self.operand2
        new = self.post_op(self.operation(op1, op2))
        return new, new % self.test_den == 0


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


class GroupDict(TypedDict):
    id: str
    items: str
    op1: str
    op2: str
    op: str
    den: str
    idt: str
    idf: str


@dataclass
class Day11(SameComputationAdventDay[list[GroupDict]]):
    @override
    def parse_input(self, input: TextIO) -> list[GroupDict]:
        return [
            cast(GroupDict, match.groupdict())
            for match in MONKEY_REGEX.finditer(input.read())
        ]

    @override
    def compute(self, var: Variant, input: list[GroupDict]) -> int:
        if var == 1:
            rounds = 20

            def post_op(x: int) -> int:
                return x // 3

        else:
            rounds = 10_000
            total = lcm(*(int(g["den"]) for g in input))

            def post_op(x: int) -> int:
                return x % total

        monkey_list = [self._parse(g, post_op) for g in input]
        monkeys: dict[int, Monkey] = {m.id: m for m in monkey_list}

        counter: Counter[int] = Counter()
        for _ in range(rounds):
            for monkey in monkeys.values():
                monkey.do_turn(counter, monkeys)

        m1, m2 = counter.most_common(2)
        return m1[1] * m2[1]

    def _parse(self, group_dict: GroupDict, post_op: Callable[[int], int]) -> Monkey:
        def _parse(val: str) -> int | Old:
            return val if val == "old" else int(val)

        items_str = [
            element
            for element in group_dict["items"].replace(" ", "").split(",")
            if element
        ]
        items = deque(item for item in map(int, items_str))

        match group_dict["op"]:
            case "+":
                operation = add
            case "*":
                operation = mul
            case _ as opd:
                raise ValueError(f"Invalid op: {opd}")

        return Monkey(
            id=int(group_dict["id"]),
            items=items,
            test_den=int(group_dict["den"]),
            if_false=int(group_dict["idf"]),
            if_true=int(group_dict["idt"]),
            operation=operation,
            operand1=_parse(group_dict["op1"]),
            operand2=_parse(group_dict["op2"]),
            post_op=post_op,
        )
