from common import BaseAdventDay, load_asset


class Day1(BaseAdventDay):
    def get_input(self, var) -> list[int]:
        data = load_asset(__file__, "calories.txt")
        calories = [0]
        for line in data:
            line = line.strip()
            if line:
                calories[-1] += int(line)
            else:
                calories.append(0)
        return (calories,)

    def run_1(self, calories: list[int]):
        return max(calories)

    def run_2(self, calories: list[int]):
        return sum(sorted(calories, reverse=True)[:3])


Instance = Day1()
