"""Day 1: Historian Hysteria (https://adventofcode.com/2024/day/1)
Code for solving part one.
"""

import pathlib


def solve(path: str) -> int:
    """Solve puzzle 01-1.

    Arguments:
        - path: path to input.

    Returns:
        The solution.
    """
    text: str = pathlib.Path(path).read_text(encoding="utf-8")
    return sum(a - b if b - a < 0 else b - a
               for a, b in zip(*map(sorted, list(zip(*[tuple(map(int, line.split("   ")))
                                                       for line in text.split("\n")])))))


if __name__ == "__main__":
    print("example:", solve("01/example01_1.txt"))
    print("input:", solve("01/input01.txt"))
