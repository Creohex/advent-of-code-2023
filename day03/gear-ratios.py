#!python

import re
from functools import reduce


def find_part_numbers(schematic, symbols):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    parts = {}

    for y, line in enumerate(schematic):
        for part_number in re.finditer(r"\d+", line):
            is_engine_part = False
            for x in range(part_number.start(), part_number.end()):
                if is_engine_part:
                    break
                for dx, dy in directions:
                    try:
                        coords = (x + dx, y + dy)
                        if schematic[coords[1]][coords[0]] in symbols:
                            parts[coords] = parts.get(coords, []) + [int(part_number.group())]
                            is_engine_part = True
                            break
                    except IndexError:
                        pass

    return parts


with open("./input", "r") as f:
    engine_schematic = f.readlines()

# part 1
print(sum(map(sum, find_part_numbers(engine_schematic, "$*&%/-@+#=").values())))

# part 2
print(sum(map(lambda l: reduce(lambda a,b: a * b, l),
              filter(lambda parts: len(parts) == 2,
                     find_part_numbers(engine_schematic, "*").values()))))
