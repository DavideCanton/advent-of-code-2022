[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)


# Advent of code 2022

Advent of code 2022 (which can be found [here](https://adventofcode.com/2022)) implemented in Python 3.

BE CAREFUL: the tests folder contains the values of the solutions for each day, so don't look in there
to avoid spoilers!

## Usage

First, install the requirements by running `pip install -r requirements.txt`.

```
$ python runner.py <day> <var>
```

where:
- `day` is the day of the advent to run
- `var` is the variant of the problem to run (defaults to 1, typically there are just 2).

## Test run

Tests can be run by using `pytest`.