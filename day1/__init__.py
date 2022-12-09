import itertools as it
from collections import defaultdict
from typing import TextIO

from common import load_asset


def _load_calories(data: TextIO) -> dict[int, int]:
    calories = defaultdict(int)
    e_id = it.count(1)
    cur = next(e_id)
    for line in data:
        line = line.strip()
        if line:
            calories[cur] += int(line)
        else:
            cur = next(e_id)
    return calories


def run(var):
    data = load_asset(__file__, "calories.txt")
    calories = _load_calories(data)
    if var == 1:
        print(max(calories.values()))
    else:
        print(sum(sorted(calories.values(), reverse=True)[:3]))
