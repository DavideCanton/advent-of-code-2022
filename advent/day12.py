from __future__ import annotations

import heapq as hq
from collections import defaultdict
from dataclasses import dataclass, field
from functools import total_ordering
from typing import DefaultDict, NamedTuple, override

from advent.common import BaseAdventDay

type Node = tuple[int, int]
type Graph = dict[Node, tuple[tuple[Node, int], ...]]


class Input(NamedTuple):
    start: Node
    goal: Node
    graph: Graph
    elevations: dict[Node, int]
    r: int
    c: int


@dataclass
@total_ordering
class HeapNode:
    dist: int
    node: Node
    valid: bool = field(init=False, default=True)

    @override
    def __eq__(self, other: object) -> bool:
        return isinstance(other, HeapNode) and self.dist == other.dist

    def __lt__(self, other: object) -> bool:
        return isinstance(other, HeapNode) and self.dist < other.dist


class HeapQueue:
    queue: list[HeapNode]
    mapping: dict[Node, HeapNode]

    def __init__(self) -> None:
        self.queue = []
        self.mapping = {}

    def pop(self) -> HeapNode | None:
        ret = None
        while self.queue:
            node = hq.heappop(self.queue)
            if node.valid:
                ret = node
                break

        if not ret:
            return None

        self.mapping.pop(ret.node)
        return ret

    def push(self, node: Node, dist: int) -> None:
        if hn := self.mapping.get(node):
            hn.valid = False

        hn = HeapNode(dist, node)
        hq.heappush(self.queue, hn)
        self.mapping[node] = hn


@dataclass
class Day12(BaseAdventDay[Input]):
    @override
    def parse_input(self) -> Input:
        def _score(c: str) -> int:
            return ord(c) - 97

        matrix = [[c for c in line.strip()] for line in self.input]

        rows = len(matrix)
        cols = len(matrix[0])

        start = goal = None
        scores = {}

        for i, row in enumerate(matrix):
            for j, c in enumerate(row):
                cur = (i, j)

                if c == "S":
                    matrix[i][j] = "a"
                    start = cur
                elif c == "E":
                    matrix[i][j] = "z"
                    goal = cur

        graph: DefaultDict[Node, list[tuple[Node, int]]] = defaultdict(list)

        for i, row in enumerate(matrix):
            for j, c in enumerate(row):
                cur = (i, j)
                cur_score = _score(c)
                scores[cur] = cur_score

                candidates: list[Node] = []
                if i > 0:
                    candidates.append((i - 1, j))
                if i < rows - 1:
                    candidates.append((i + 1, j))
                if j > 0:
                    candidates.append((i, j - 1))
                if j < cols - 1:
                    candidates.append((i, j + 1))

                for c in candidates:
                    s = _score(matrix[c[0]][c[1]])
                    if s - cur_score <= 1:
                        graph[c].append((cur, 1))

        assert start is not None
        assert goal is not None

        return Input(start, goal, {k: tuple(v) for k, v in graph.items()}, scores, rows, cols)

    def _find_path(self, start: Node, graph: Graph) -> dict[Node, int]:
        _M = 99999
        dist: dict[Node, int] = defaultdict(lambda: _M)

        queue = HeapQueue()
        for n in graph:
            queue.push(n, _M)
        queue.push(start, 0)

        while True:
            cur_n = queue.pop()
            if not cur_n:
                break
            cur = cur_n.node
            cur_d = cur_n.dist

            for adj, weight in graph.get(cur, ()):
                adj_dist = dist[adj]
                adj_new_dist = cur_d + weight

                if adj_new_dist < adj_dist:
                    dist[adj] = adj_new_dist
                    queue.push(adj, adj_new_dist)

        return dist

    @override
    def _run_1(self, input: Input) -> int:
        res = self._find_path(input.goal, input.graph)
        assert res is not None
        return res[input.start]

    @override
    def _run_2(self, input: Input) -> int:
        r = self._find_path(input.goal, input.graph)
        a = {r[n] for n, e in input.elevations.items() if e == 0}

        return min(a)
