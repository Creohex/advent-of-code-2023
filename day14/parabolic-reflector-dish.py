#!python

from typing import Generator


def parse_rocks():
    with open("./input", "r") as f:
        dish = list(map(str.strip, f.readlines()))
    height = len(dish)
    width = len(dish[0])
    rocks = dict()
    for y in range(height):
        for x in range(width):
            if dish[y][x] in "#O":
                rocks[(x, y)] = dish[y][x]
    return rocks, height, width


rocks, height, width = parse_rocks()
tilt_directions = [
    ((0, -1), lambda: ((x, y) for y in range(1, height) for x in range(width))),
    ((-1, 0), lambda: ((x, y) for x in range(1, width) for y in range(height))),
    ((0, 1), lambda: ((x, y) for y in reversed(range(height - 1)) for x in range(width))),
    ((1, 0), lambda: ((x, y) for x in reversed(range(width - 1)) for y in range(height))),
]
"""North, West, South, East"""


def visualize(rocks: dict) -> None:
    dish = ("".join(rocks.get((x, y), ".") for x in range(width)) for y in range(height))
    print("\n".join(dish))


def hashed(rocks: dict) -> str:
    return "".join(
        "".join(rocks.get((x, y), ".") for x in range(width)) for y in range(height)
    )


def calculate_weight(rocks: dict) -> int:
    return sum(height - y for _, y in filter(lambda coord: rocks[coord] == "O", rocks))


def tilt(rocks: dict, direction: tuple, coords_gen: Generator) -> None:
    dx, dy = direction

    for x, y in coords_gen():
        if rocks.get((x, y)) == "O":
            steps = 0

            while True:
                next_x = x + dx * (steps + 1)
                next_y = y + dy * (steps + 1)

                if not (
                    0 <= next_x < width
                    and 0 <= next_y < height
                    and (next_x, next_y) not in rocks
                ):
                    break

                steps += 1

            if steps:
                del rocks[(x, y)]
                rocks[(x + dx * steps, y + dy * steps)] = "O"


def spin(rocks: dict) -> None:
    iteration = 0
    weights = dict()

    while iteration < 1_000_000_000:
        hashed_rocks = hashed(rocks)
        if hashed_rocks in weights:
            weight = weights[hashed_rocks]
            cycle_start = weight[0]
            idx = (1_000_000_000 - cycle_start) % (iteration - cycle_start) + cycle_start
            return next(weight for i, weight in weights.values() if i == idx)

        weights[hashed_rocks] = (iteration, calculate_weight(rocks))
        [tilt(rocks, *tilt_data) for tilt_data in tilt_directions]
        iteration += 1


# part 1:
r = rocks.copy()
tilt(r, *tilt_directions[0])
print(calculate_weight(r))

# part 2:
print(spin(rocks))
