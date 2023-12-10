#!python

import math
import re
from functools import partial, reduce
from itertools import cycle


def parse_input(raw_input):
    instructions, raw_map = raw_input.split("\n\n")
    network = {}
    for line in raw_map.splitlines():
        node, left, right = re.findall(r"\w+", line)
        network[node] = (left, right)
    return cycle(instructions), network

with open("./input", "r") as f:
    instructions, network = parse_input(f.read())

def traverse(node, end):
    steps = 0
    while not node.endswith(end):
        steps += 1
        node = network[node][0 if next(instructions) == "L" else 1]
    return steps


# part 1:
print(traverse("AAA", "ZZZ"))

# part 2:
traverse_z = partial(traverse, end="Z")
print(reduce(lambda a,b: a * b // math.gcd(a, b),  # LCM
             map(traverse_z,
                 filter(lambda n: n.endswith("A"),
                        network))))
