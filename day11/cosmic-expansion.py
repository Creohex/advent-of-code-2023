#!python

from itertools import combinations


def parse_galaxies(universe: list, distance_multiplicator: int) -> dict:
    galaxies = {}
    height = len(universe)
    width = len(universe[0])

    for y in range(height):
        for x in range(width):
            if universe[y][x] == "#":
                galaxies[len(galaxies) + 1] = (x, y)

    empty_columns = set(range(width)).difference(coord[0] for coord in galaxies.values())
    empty_rows = set(range(height)).difference(coord[1] for coord in galaxies.values())

    for num, (x, y) in galaxies.items():
        x_offset = len(list(filter(lambda v: v in empty_columns, range(x))))
        y_offset = len(list(filter(lambda v: v in empty_rows, range(y))))
        galaxies[num] = (
            (x - x_offset) + x_offset * distance_multiplicator,
            (y - y_offset) + y_offset * distance_multiplicator,
        )

    return galaxies


def calculate_distances(galaxies: dict) -> list:
    distances = [
        abs(xb - xa) + abs(yb - ya)
        for (xa, ya), (xb, yb) in combinations(galaxies.values(), 2)
    ]
    return sum(distances)


with open("./input", "r") as f:
    universe = f.readlines()

# part 1:
print(calculate_distances(parse_galaxies(universe, 2)))

# part 2:
print(calculate_distances(parse_galaxies(universe, 1_000_000)))
