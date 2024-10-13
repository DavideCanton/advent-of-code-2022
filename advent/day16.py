from __future__ import annotations

import re
from dataclasses import dataclass
from itertools import permutations, product
from typing import override

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
    opened: frozenset[Node]
    remaining: frozenset[Node]
    pos: str
    t: int
    current_best: int


DistanceMatrix = dict[tuple[str, str], int]


@dataclass
class Day16(BaseAdventDay[Graph]):
    REGEX = re.compile(r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)")

    @override
    def parse_input(self) -> Graph:
        graph = Graph()

        for line in self.input:
            if (match := self.REGEX.match(line)) is None:
                continue

            valve, rate, out_valves = match.groups()
            graph.add_node(Node(valve, int(rate)))
            for out_valve in out_valves.split(", "):
                graph.add_edge(valve, out_valve)

        graph.check()
        return graph

    @override
    def _run_1(self, input: Graph):
        start = State(
            opened=frozenset(),
            remaining=frozenset(n for n in input.nodes.values() if n.rate > 0),
            pos="AA",
            t=0,
            current_best=0,
        )

        dist = self._compute_distance_matrix(input)
        ans = self._visit(start, dist, 30, {})
        return max(ans.values())

    @override
    def _run_2(self, input: Graph):
        dist = self._compute_distance_matrix(input)
        start_valve = "AA"

        start = State(
            opened=frozenset(),
            remaining=frozenset(n for n in input.nodes.values() if n.rate > 0),
            pos=start_valve,
            t=0,
            current_best=0,
        )
        ans = self._visit(start, dist, 26, {})

        return max(m1 + m2 for k1, m1 in ans.items() for k2, m2 in ans.items() if not k1 & k2)

    def _compute_distance_matrix(self, input: Graph) -> DistanceMatrix:
        dist = {
            (i, j): 1 if j in input.edges[i] else 100000
            for i, j in product(input.nodes, repeat=2)
            if i != j
        }

        for k, i, j in permutations(input.nodes, 3):
            dist[i, j] = min(dist[i, j], dist[i, k] + dist[k, j])
        return dist

    def _visit(
        self,
        state: State,
        dist: DistanceMatrix,
        max_time: int,
        res: dict[frozenset[Node], int],
    ) -> dict[frozenset[Node], int]:
        res[state.opened] = max(res.get(state.opened, 0), state.current_best)

        if state.t == max_time or not state.remaining:
            return res

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
            self._visit(next_state, dist, max_time, res)

        return res
