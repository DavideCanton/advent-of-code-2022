from __future__ import annotations

import importlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .common import BaseAdventDay

CLASSES: dict[int, type[BaseAdventDay]] = {}


def _init():
    for i in range(1, 26):
        try:
            mod = importlib.import_module(f"advent.day{i}")
            cls = getattr(mod, f"Day{i}")
            CLASSES[i] = cls
        except ImportError:
            pass


_init()
