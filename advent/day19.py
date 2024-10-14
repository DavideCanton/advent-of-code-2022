from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Self, override

from advent.common import BaseAdventDay

PATTERN: re.Pattern[str] = re.compile(
    r"Blueprint (\d+): Each ore robot costs (\d+) ore\. Each clay robot costs (\d+) ore\. "
    r"Each obsidian robot costs (\d+) ore and (\d+) clay\. "
    r"Each geode robot costs (\d+) ore and (\d+) obsidian\.",
)


@dataclass
class Blueprint:
    id: int
    costs: tuple[
        tuple[int, int, int],
        tuple[int, int, int],
        tuple[int, int, int],
        tuple[int, int, int],
    ]

    @classmethod
    def from_string(cls, blueprint: str) -> Self:
        match = PATTERN.match(blueprint)
        if not match:
            raise ValueError(f"Invalid blueprint: {blueprint}")

        id = int(match.group(1))
        costs = tuple(int(match.group(i)) for i in range(2, 8))
        assert len(costs) == 6
        return cls(
            id,
            (
                (costs[0], 0, 0),
                (costs[1], 0, 0),
                (costs[2], costs[3], 0),
                (costs[4], 0, costs[5]),
            ),
        )


@dataclass(frozen=True)
class State:
    robots: tuple[int, int, int, int]
    resources: tuple[int, int, int]
    geodes: int
    minutes: int
    total_minutes: int

    __slots__ = ("robots", "resources", "geodes", "minutes", "total_minutes")

    def new_state_buying(self, blueprint: Blueprint, index: int) -> State | None:
        cost = blueprint.costs[index]

        if all(r >= c for r, c in zip(self.resources, cost)):
            new_robots = list(self.robots)
            new_robots[index] += 1
            new_robots = tuple(new_robots)
            assert len(new_robots) == 4

            new_resources = tuple(self.resources[i] - cost[i] + self.robots[i] for i in range(3))
            assert len(new_resources) == 3

            geodes = self.geodes + self.robots[3]

            return State(new_robots, new_resources, geodes, self.minutes - 1, self.total_minutes)
        else:
            return None

    def new_state_not_buying(self) -> State | None:
        new_resources = tuple(self.resources[i] + self.robots[i] for i in range(3))
        assert len(new_resources) == 3
        geodes = self.geodes + self.robots[3]

        return State(self.robots, new_resources, geodes, self.minutes - 1, self.total_minutes)


@dataclass
class Day19(BaseAdventDay[list[Blueprint]]):
    @override
    def parse_input(self) -> list[Blueprint]:
        return [Blueprint.from_string(line) for line in self.input]

    @override
    def _run_1(self, input: list[Blueprint]):
        tot = 0
        minutes = 24
        for bp in input:
            initial_state = State((1, 0, 0, 0), (0, 0, 0), 0, minutes, minutes)
            visited: dict[State, int] = {}
            geodes = self._simulate(bp, initial_state, visited)
            tot += bp.id * geodes
        return tot

    @override
    def _run_2(self, input: list[Blueprint]):
        pass

    def _simulate(self, blueprint: Blueprint, state: State, visited: dict[State, int]) -> int:
        new_states = [state.new_state_buying(blueprint, i) for i in range(4)] + [
            state.new_state_not_buying()
        ]

        geodes: list[int] = []
        for s in new_states:
            if s is None:
                continue

            if s.minutes == 0 or s in visited:
                g = s.geodes
            else:
                g = self._simulate(blueprint, s, visited)

            visited[s] = g
            geodes.append(g)

        return max(geodes, default=0)
