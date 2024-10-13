from __future__ import annotations

from abc import ABCMeta, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from functools import cached_property
from typing import TextIO, TypeGuard, override

from advent.common import BaseAdventDay


@dataclass
class Entry(metaclass=ABCMeta):
    name: str

    @property
    @abstractmethod
    def size(self) -> int: ...

    @abstractmethod
    def list_dirs(self) -> Iterable[Dir]: ...


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
class Dir(Entry):
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
    def size(self) -> int:  # pyright: ignore [reportIncompatibleMethodOverride]
        return sum(e.size for e in self.children.values())

    def list_dirs(self) -> Iterable[Dir]:
        yield self
        for e in self.children.values():
            yield from e.list_dirs()

    def _check_child(self, name: str):
        if name in self.children:
            raise ValueError(f"Directory {self.name} has already a child named {name}")

    def _invalidate_caches(self):
        cur = self
        while cur:
            cur.__dict__.pop("size", None)
            cur = cur.parent


@dataclass
class Day7(BaseAdventDay[Dir]):
    @override
    def parse_input(self, input: TextIO) -> Dir:
        root = Dir.root()
        cur = None
        it = iter(input)  # type: ignore

        end_of_file = object()
        command = next(it, end_of_file)

        while command is not end_of_file:
            assert self._is_command(command)
            command = command[1:].strip()

            output: list[str] = []
            if command == "ls":
                while True:
                    row = next(it, end_of_file)
                    if row is end_of_file or self._is_command(row):
                        next_command = row
                        break
                    else:
                        assert isinstance(row, str)
                        output.append(row.strip())
            else:
                next_command = next(it, end_of_file)

            cur = self._apply_command(command, output, cur, root)
            command = next_command

        return root

    @override
    def _run_1(self, input: Dir) -> int:
        return sum(d.size for d in input.list_dirs() if d.size <= 100000)

    @override
    def _run_2(self, input: Dir) -> int:
        total_space = 70_000_000
        free_space = total_space - input.size
        to_clean = 30_000_000 - free_space

        return min((d for d in input.list_dirs() if d.size >= to_clean), key=lambda d: d.size).size

    def _apply_command(self, command: str, output: list[str], cur: Dir | None, root: Dir) -> Dir:
        match command.split():
            case ["ls"]:
                assert cur is not None
                for line in output:
                    self._update(cur, line)
                return cur
            case ["cd", t] if t == ROOT:
                return root
            case ["cd", t] if t == "..":
                assert cur is not None
                if cur.parent is None:
                    raise ValueError("Parent of root is not defined")
                return cur.parent
            case ["cd", t]:
                assert cur is not None
                dir = next((c for name, c in cur.children.items() if name == t), None)
                if dir:
                    assert isinstance(dir, Dir)
                    return dir
                raise ValueError(f"Directory {cur.name} has no child named {t}.")
            case _:
                raise ValueError(f"Invalid command: {command}")

    def _update(self, cur: Dir, line: str) -> None:
        match line.split():
            case ["dir", dir_name]:
                cur.child(dir_name)
            case [size, file_name]:
                cur.file(file_name, int(size))
            case _:
                raise ValueError(line)

    def _is_command(self, row: str | object) -> TypeGuard[str]:
        return isinstance(row, str) and row[0] == "$"
