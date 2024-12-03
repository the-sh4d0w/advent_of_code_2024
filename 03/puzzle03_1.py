"""Day 3: Mull It Over (https://adventofcode.com/2024/day/3)
Code for solving part one.
"""

import pathlib
import re


def mul(a: int, b: int) -> int:
    """Multiply two values."""
    return a * b


def solve(path: str) -> int:
    """Solve puzzle 03-1.

    Arguments:
        - path: path to input.

    Returns:
        The solution.
    """
    text = pathlib.Path(path).read_text(encoding="utf-8")
    return sum(map(eval, re.findall(r"mul\([0-9]+,[0-9]+\)", text)))


if __name__ == "__main__":
    print("example:", solve("03/example03_1.txt"))
    print("input:", solve("03/input03.txt"))
