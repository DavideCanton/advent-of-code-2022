# type: ignore
from line_profiler import LineProfiler

from advent import get_handler_for_day
from runner import _run

profile = LineProfiler()

day = 16
variant = 1

fns = []
handler = get_handler_for_day(day)

if variant == 1:
    fns.append(handler._run_1)
elif variant == 2:
    fns.append(handler._run_2)

# add functions to be profiled here

for fn in fns:
    if hasattr(fn, "__wrapped__"):
        fn = fn.__wrapped__
    profile.add_function(fn)


def main():
    _run(day, variant)


profile.runcall(main)
profile.print_stats()
