"""Day 1: Historian Hysteria (https://adventofcode.com/2024/day/1#part2)
Code for solving part two.
"""

import pathlib


def solve(path: str) -> int:
    """Solve puzzle 01-2.

    Arguments:
        - path: path to input.

    Returns:
        The solution.
    """
    text = pathlib.Path(path).read_text(encoding="utf-8")
    left, right = list(map(list, zip(*[tuple(map(int, line.split("   ")))
                                       for line in text.split("\n")])))
    return sum(num * right.count(num) for num in left)


if __name__ == "__main__":
    print("example:", solve("01/example01_2.txt"))
    print("input:", solve("01/input01.txt"))
