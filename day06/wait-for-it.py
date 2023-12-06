#!python

import re
from typing import Iterable


test = """\
Time:      7  15   30
Distance:  9  40  200
"""

data = """\
Time:        54     81     70     88
Distance:   446   1292   1035   1007
"""


def parse_input(source: str, fixed_kerning: bool=False) -> Iterable[tuple]:
    vals = list(map(int, re.findall(r"\d+", source.replace(" ", "")
                                    if fixed_kerning else source)))
    return zip(vals[:len(vals)//2], vals[len(vals)//2:])

def solve(rounds: Iterable[tuple]) -> int:
    result = 1
    for time, target_distance in rounds:
        speed = 0
        times_over_record = 0
        for dt in range(time):
            if speed * (time - dt) > target_distance:
                times_over_record += 1
            speed += 1
        result *= times_over_record
    return result


# part 1:
print(solve(parse_input(data)))

# part 2:
print(solve(parse_input(data, fixed_kerning=True)))
