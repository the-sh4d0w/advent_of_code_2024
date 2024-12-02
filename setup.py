"""Automatically set up file structure for a day of advent of code.
Also download necessaray examples and input.
"""

import argparse
import datetime
import pathlib
import sys
import time
import typing

import bs4
import click
import requests

DOMAIN = "adventofcode.com"
SESSION_PATH = "session.cookie"
TODAY = datetime.date.today()
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
CODE_PLACEHOLDER = '''"""{title} ({url})
Code for solving part {part_word}.
"""

import pathlib


def solve(path: str) -> str:
    """Solve puzzle {day:02}-{part}.

    Arguments:
        - path: path to input.

    Returns:
        The solution.
    """
    text = pathlib.Path(path).read_text(encoding="utf-8")
    return text


if __name__ == "__main__":
    print("example:", solve("{day:02}/example{day:02}_{part}.txt"))
    print("input:", solve("{day:02}/input{day:02}.txt"))
'''

# setup arg parser
arg_parser = argparse.ArgumentParser(description="Automatically download files"
                                     " and set up folder and files for a day"
                                     " of advent of code.", epilog="Session"
                                     " cookie is expected to be in the file"
                                     f" '{SESSION_PATH}'.")
arg_parser.add_argument("-d", "--day", type=int, choices=range(1, 26),
                        metavar="DAY", default=TODAY.day,
                        help="Day of advent of code.")
arg_parser.add_argument("-y", "--year", type=int, default=TODAY.year,
                        choices=range(2015, TODAY.year+1), metavar="YEAR",
                        help="Year of advent of code.")
arg_parser.add_argument("-p", "--part", type=int, choices=range(1, 3),
                        default=1, metavar="PART", help="Part of the task.")
arg_parser.add_argument("-w", "--wait", action="store_true", default=False,
                        help="Wait until task is available.")
arg_parser.add_argument("-n", "--ntfy", default=False, help="Send "
                        "notification when finished (for use with wait).")


@click.command(epilog=f"Session cookie is expected to be in the file '{SESSION_PATH}'.")
@click.option("-d", "--day", type=click.IntRange(0, 25), default=TODAY.day,
              help="Day of advent of code.")
@click.option("-y", "--year", type=click.IntRange(
    2015, TODAY.year if TODAY.month == 12 else TODAY.year - 1), default=TODAY.year,
    help="Year of advent of code.")
@click.option("-p", "--part", type=click.IntRange(1, 2), default=1, help="Part of the task.")
@click.option("-w", "--wait", is_flag=True, help="Wait until task is available.")
@click.option("-n", "--notify", is_flag=True, help="Send notification when finished.")
@click.option("--ntfy_url", type=str, show_default=True, default="http://olympus:1234/aoc",
              help="URL for ntfy.")
def main(day: int, year: int, part: int, wait: bool, notify: bool, ntfy_url: str) -> None:
    """Automatically download files and set up folder and files for a day of advent of code."""
    # wait until release of task; +30 seconds to prevent bug
    if wait and datetime.datetime(year, 12, day, 6) > datetime.datetime.now():
        print("Waiting until task releases at "
              f"{year}-12-{day}T06:00:00+01:00.")
        time.sleep((datetime.datetime(year, 12, day, 6)
                    - datetime.datetime.now()).total_seconds() + 30)
    url = f"https://{DOMAIN}/{year}/day/{day}"
    file = pathlib.Path(SESSION_PATH)

    # exit if session cookie file doesn't exist
    if not file.exists():
        sys.exit(f"The file '{SESSION_PATH}' does not exist.")

    # get session token
    session = file.read_text(encoding="utf-8").strip()

    # download example(s) and input
    with requests.Session() as sess:
        # set session token
        sess.cookies.set(name="session", value=session, domain=DOMAIN)
        response = sess.get(url)
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        title = typing.cast(bs4.Tag, soup.find("h2")
                            ).text.replace("-", "").strip()
        examples = [typing.cast(bs4.Tag, code).text.strip()
                    for code in soup.find_all("code") if "\n" in code.text]
        input_text = sess.get(f"{url}/input").text.strip()

    # exit with error if part two not available
    if part == 2 and not "Part Two" in response.text:
        sys.exit("Part two is not yet available.")

    # setup folder and files
    format_values = {
        "title": title,
        "url": url + ("#part2" if part == 2 else ""),
        "part_word": "one" if part == 1 else "two",
        "day": day,
        "part": part
    }
    pathlib.Path(f"{day:02}").mkdir(exist_ok=True)
    pathlib.Path(f"{day:02}/puzzle{day:02}_{part}.py").write_text(
        data=CODE_PLACEHOLDER.format_map(format_values), encoding="utf-8")
    pathlib.Path(f"{day:02}/example{day:02}_{part}.txt").write_text(
        data=examples[part - 1 if len(examples) != 1 else 0], encoding="utf-8")
    pathlib.Path(f"{day:02}/input{day:02}.txt").write_text(
        data=input_text, encoding="utf-8")

    # send notification
    if notify:
        requests.post(ntfy_url, timeout=10,
                      data=f"Part {part} of {year}-12-{day:02} finished downloading.",
                      headers={"Title": "Advent of Code Setup", "Tags": "christmas_tree"})


if __name__ == "__main__":
    main()  # pylint:disable=no-value-for-parameter
