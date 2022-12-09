from common import load_asset

P = "RPS"
OPPONENT = dict(zip("ABC", P))
SCORES = dict(zip(P, range(1, 4)))

WINS = {"S": "P", "R": "S", "P": "R"}
LOSES = {v: k for k, v in WINS.items()}


def _compute_score(io, iy):
    if io == iy:
        return 3
    elif WINS[io] == iy:
        return 0
    else:
        return 6


class Result1:
    def __init__(self):
        self.yours_table = dict(zip("XYZ", P))

    def __call__(self, opp, yours):
        io = OPPONENT[opp]
        iy = self.yours_table[yours]

        return SCORES[iy] + _compute_score(io, iy)


class Result2:
    def __call__(self, opp, result):
        io = OPPONENT[opp]
        match result:
            case "Y":
                iy = io
            case "X":
                iy = WINS[io]
            case "Z":
                iy = LOSES[io]

        return SCORES[iy] + _compute_score(io, iy)


def run(var):
    if var == 1:
        fn = Result1()
    else:
        fn = Result2()

    tot = sum(fn(*row.strip().split()) for row in load_asset(__file__, "strategy.txt"))
    print(tot)
