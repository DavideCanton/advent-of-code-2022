import importlib


class Base:
    def _create_case(self, request):
        index = request.param
        return (index + 1, self.DATA[index])

    def test(self, test_cases):
        variant, exp = test_cases
        module = importlib.import_module(f"advent.day{self.DAY}")
        res = module.Instance.run(variant)
        assert res == exp
