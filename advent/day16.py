from __future__ import annotations

import re
from dataclasses import dataclass
from itertools import permutations, product
from typing import TextIO

from advent.common import BaseAdventDay


@dataclass(slots=True, unsafe_hash=True)
class Node:
    name: str
    rate: int


class Graph:
    nodes: dict[str, Node]
    edges: dict[str, set[str]]

    def __init__(self) -> None:
        self.nodes = {}
        self.edges = {}

    def add_node(self, n: Node):
        self.nodes[n.name] = n
        self.edges[n.name] = set()

    def add_edge(self, f: str, t: str):
        self.edges[f].add(t)

    def check(self):
        for nf, nts in self.edges.items():
            assert nf in self.nodes, nf
            for nt in nts:
                assert nt in self.nodes, nt


@dataclass(slots=True)
class State:
    opened: set[Node]
    remaining: set[Node]
    pos: str
    t: int
    current_best: int


@dataclass
class Day16(BaseAdventDay[Graph]):
    day = 16

    REGEX = re.compile(
        r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)"
    )

    def parse_input(self, input: TextIO) -> Graph:
        graph = Graph()

        for line in input:
            if (match := self.REGEX.match(line)) is None:
                continue

            valve, rate, out_valves = match.groups()
            graph.add_node(Node(valve, int(rate)))
            for out_valve in out_valves.split(", "):
                graph.add_edge(valve, out_valve)

        graph.check()
        return graph

    def _run_1(self, input: Graph):
        start = State(
            opened=set(),
            remaining={n for n in input.nodes.values() if n.rate > 0},
            pos="AA",
            t=0,
            current_best=0,
        )

        dist = {
            (i, j): 1 if j in input.edges[i] else 100000
            for i, j in product(input.nodes, repeat=2)
            if i != j
        }

        for k, i, j in permutations(input.nodes, 3):
            dist[i, j] = min(dist[i, j], dist[i, k] + dist[k, j])

        return self._visit(start, dist, 30)

    def _run_2(self, input: Graph):
        pass

    def _visit(
        self, state: State, dist: dict[tuple[str, str], int], max_time: int
    ) -> int:
        if state.t == max_time or not state.remaining:
            return state.current_best

        ns: list[int] = []
        cur = state.pos
        for adj in state.remaining:
            next_t = state.t + dist[cur, adj.name] + 1
            if next_t > max_time:
                continue

            next_state = State(
                opened=state.opened | {adj},
                remaining=state.remaining - {adj},
                pos=adj.name,
                t=next_t,
                current_best=state.current_best + (max_time - next_t) * adj.rate,
            )
            ns.append(self._visit(next_state, dist, max_time))

        return max(ns, default=0)
