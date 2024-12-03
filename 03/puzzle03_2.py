"""Day 3: Mull It Over (https://adventofcode.com/2024/day/3#part2)
Code for solving part two.
"""

import pathlib
import re


class Value:
    """Yes, I know this is stupid."""
    enabled = True


def mul(a: int, b: int) -> int:
    """Multiply two values."""
    return a * b if Value.enabled else 0


def do() -> int:
    """Enable mul function"""
    Value.enabled = True
    return 0


def dont() -> int:
    """Enable mul function"""
    Value.enabled = False
    return 0


def solve(path: str) -> int:
    """Solve puzzle 03-2.

    Arguments:
        - path: path to input.

    Returns:
        The solution.
    """
    text = pathlib.Path(path).read_text(encoding="utf-8")
    return sum(map(eval, re.findall(r"(mul\([0-9]+,[0-9]+\)|do\(\)|dont\(\))",
                                    text.replace("'", ""))))


if __name__ == "__main__":
    print("example:", solve("03/example03_2.txt"))
    print("input:", solve("03/input03.txt"))
