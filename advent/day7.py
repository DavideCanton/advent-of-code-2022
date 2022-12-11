from __future__ import annotations

from abc import ABCMeta, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from functools import cached_property
from typing import TextIO

from advent.common import BaseAdventDay


@dataclass
class Entry(metaclass=ABCMeta):
    name: str

    @property
    @abstractmethod
    def size(self) -> int:
        ...

    @abstractmethod
    def list_dirs(self) -> Iterable[Dir]:
        ...


@dataclass
class File(Entry):
    _size: int

    @property
    def size(self) -> int:
        return self._size

    def list_dirs(self) -> Iterable[Dir]:
        yield from ()


ROOT = "/"


@dataclass
class Dir:
    name: str
    children: dict[str, Entry]
    parent: Dir | None

    @classmethod
    def root(cls):
        return cls(ROOT, {}, None)

    def child(self, name: str) -> Dir:
        self._check_child(name)
        new = Dir(name, {}, self)
        self.children[name] = new
        self._invalidate_caches()
        return new

    def file(self, name: str, size: int) -> File:
        self._check_child(name)
        file = self.children[name] = File(name, size)
        self._invalidate_caches()
        return file

    @cached_property
    def size(self) -> int:
        return sum(e.size for e in self.children.values())

    def list_dirs(self) -> Iterable[Dir]:
        yield self
        for e in self.children.values():
            yield from e.list_dirs()

    def _check_child(self, name):
        if name in self.children:
            raise ValueError(f"Directory {self.name} has already a child named {name}")

    def _invalidate_caches(self):
        cur = self
        while cur:
            cur.__dict__.pop("size", None)
            cur = cur.parent


@dataclass
class Day7(BaseAdventDay):
    day = 7

    def parse_input(self, input: TextIO) -> Dir:
        root = Dir.root()
        cur = None
        it = iter(input)

        end_of_file = object()
        command = next(it, end_of_file)

        while command is not end_of_file:
            assert self._is_command(command)
            command = command[1:].strip()

            output = []
            if command == "ls":
                while True:
                    row = next(it, end_of_file)
                    if row is end_of_file or self._is_command(row):
                        next_command = row
                        break
                    else:
                        output.append(row.strip())
            else:
                next_command = next(it, end_of_file)

            cur = self._apply_command(command, output, cur, root)
            command = next_command

        return root

    def run_1(self, root: Dir) -> int:
        return sum(s for d in root.list_dirs() if (s := d.size) <= 100000)

    def run_2(self, root: Dir) -> int:
        total_space = 70000000
        free_space = total_space - root.size
        to_clean = 30000000 - free_space

        return min(
            (d for d in root.list_dirs() if d.size >= to_clean), key=lambda d: d.size
        ).size

    def _apply_command(
        self, command: str, output: list[str], cur: Dir | None, root: Dir
    ) -> Dir:
        match command.split():
            case ["ls"]:
                for line in output:
                    assert cur is not None
                    self._update(cur, line)
                return cur
            case ["cd", t] if t == ROOT:
                return root
            case ["cd", t] if t == "..":
                assert cur is not None
                return cur.parent
            case ["cd", t]:
                assert cur is not None
                if any((d := c) for name, c in cur.children.items() if name == t):
                    assert isinstance(d, Dir)
                    return d
                raise ValueError(f"Directory {cur.name} has no child named {t}.")
            case _:
                raise ValueError(f"Invalid command: {command}")

    def _update(self, cur: Dir, line: str) -> None:
        match line.split():
            case ["dir", dir_name]:
                cur.child(dir_name)
            case [size, file_name]:
                cur.file(file_name, int(size))

    def _is_command(self, row: str) -> bool:
        return row[0] == "$"


ProblemClass = Day7
