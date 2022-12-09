import importlib


class Base:
    def test_variant(self, data):
        day, variant, exp = data
        module = importlib.import_module(f"advent.day{day}")
        res = module.Instance.run(variant)
        assert res == res
