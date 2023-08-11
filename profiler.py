from line_profiler import LineProfiler

from advent.day14 import Board, Path
from runner import main

profile = LineProfiler()

# add functions to be profiled here
fns = [Board._is_blocked, Path.__contains__]
for f in fns:
    if hasattr(f, "__wrapped__"):
        f = f.__wrapped__
    profile.add_function(f)

profile.runcall(main)
profile.print_stats()
