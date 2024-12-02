"""Day 2: RedNosed Reports (https://adventofcode.com/2024/day/2#part2)
Code for solving part two.
"""

import pathlib


def solve(path: str) -> int:
    """Solve puzzle 02-2.

    Arguments:
        - path: path to input.

    Returns:
        The solution.
    """
    text = pathlib.Path(path).read_text(encoding="utf-8")
    return sum(any(all(0 < levels[i+1] - levels[i] < 4 for i in range(len(levels)-1))
               or all(0 < levels[i] - levels[i+1] < 4 for i in range(len(levels)-1))
               for levels in [levels[:i] + levels[i+1:] for i in range(len(levels))])
               for levels in [list(map(int, line.split())) for line in text.split("\n")])


if __name__ == "__main__":
    print("example:", solve("02/example02_2.txt"))
    print("input:", solve("02/input02.txt"))
