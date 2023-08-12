from __future__ import annotations

import re
from collections import deque
from dataclasses import dataclass, field
from typing import ClassVar, TextIO

from advent.common import BaseAdventDay


@dataclass(frozen=True)
class Node:
    name: str
    rate: int
    id: int = field(init=False)
    _ID: ClassVar[int] = 0

    def __post_init__(self):
        object.__setattr__(self, "id", self._ID)
        self.__class__._ID += 1


class Graph:
    nodes: dict[str, Node]
    edges: dict[str, set[str]]
    nodes_by_id: dict[int, Node]

    def __init__(self) -> None:
        self.nodes = {}
        self.edges = {}
        self.nodes_by_id = {}

    def add_node(self, n: Node):
        self.nodes[n.name] = n
        self.nodes_by_id[n.id] = n
        self.edges[n.name] = set()

    def add_edge(self, f: str, t: str):
        self.edges[f].add(t)

    def check(self):
        for nf, nts in self.edges.items():
            assert nf in self.nodes, nf
            for nt in nts:
                assert nt in self.nodes, nt


class BitSet:
    state: int

    def __init__(self, initial: int | None = None) -> None:
        self.state = initial or 0

    def copy(self) -> BitSet:
        return BitSet(self.state)

    def __or__(self, other: set[int]) -> BitSet:
        copy = self.copy()
        for v in other:
            copy[v] = True
        return copy

    def __getitem__(self, n: int) -> bool:
        return bool(1 << n & self.state)

    def __setitem__(self, n: int, val: bool) -> None:
        mask = 1 << n
        if val:
            self.state |= mask
        else:
            self.state &= ~mask

    def __iter__(self):
        v = self.state
        n = 0
        while v:
            if v & 1:
                yield n
            v >>= 1
            n += 1

    def __repr__(self) -> str:
        return str(sorted(self))

    __contains__ = __getitem__


@dataclass(slots=True)
class State:
    opened: BitSet
    pos: str
    prev: str | None
    t: int
    current_pressure: int


@dataclass
class Day16(BaseAdventDay[Graph]):
    day = 16

    REGEX = re.compile(
        r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)"
    )

    def parse_input(self, input: TextIO) -> Graph:
        g = Graph()
        for line in input:
            if m := self.REGEX.match(line):
                v, r, vs = m.groups()
                g.add_node(Node(v, int(r)))
                for vv in vs.split(", "):
                    g.add_edge(v, vv)
        g.check()
        return g

    def _run_1(self, input: Graph):
        queue = deque([State(BitSet(), "AA", None, 0, 0)])
        cur_max = -1

        ins = queue.append
        rem = queue.pop

        while queue:
            cur = rem()

            if cur.t == 30:
                if cur.current_pressure > cur_max:
                    cur_max = cur.current_pressure
                continue

            node = input.nodes[cur.pos]
            new_pressure = cur.current_pressure + sum(
                input.nodes_by_id[v].rate for v in cur.opened
            )

            if node.id not in cur.opened and node.rate > 0:
                ins(
                    State(
                        cur.opened | {node.id}, cur.pos, None, cur.t + 1, new_pressure
                    )
                )

            for adj in input.edges[cur.pos]:
                if adj != cur.prev:
                    ins(State(cur.opened, adj, cur.pos, cur.t + 1, new_pressure))

        return cur_max

    def _run_2(self, input: Graph):
        pass
