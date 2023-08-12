from line_profiler import LineProfiler

from advent.day16 import Day16
from runner import main

profile = LineProfiler()

# add functions to be profiled here
fns = [Day16._run_1, Day16._visit]
for f in fns:
    if hasattr(f, "__wrapped__"):
        f = f.__wrapped__
    profile.add_function(f)

profile.runcall(main)
profile.print_stats()
