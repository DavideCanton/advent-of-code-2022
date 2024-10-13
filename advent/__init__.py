from __future__ import annotations

import importlib
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .common import BaseAdventDay

_CLASSES: dict[int, type[BaseAdventDay[Any]]] = {}


def _init():
    for i in range(1, 26):
        try:
            mod = importlib.import_module(f"advent.day{i}")
            cls = getattr(mod, f"Day{i}")
            _CLASSES[i] = cls
        except ImportError:
            pass


_init()


def get_handler_for_day(day: int) -> type[BaseAdventDay[Any]]:
    return _CLASSES[day]
