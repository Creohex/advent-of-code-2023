#!python

from itertools import chain


class Coord(tuple):
    def __add__(self, other):
        return Coord(a + b for a, b in zip(self, other))


up = "up"
down = "down"
left = "left"
right = "right"

directions = {
    up: Coord((0, -1)),
    down: Coord((0, 1)),
    left: Coord((-1, 0)),
    right: Coord((1, 0)),
}

reflections = {
    "/": {down: (left,), up: (right,), right: (up,), left: (down,)},
    "\\": {down: (right,), up: (left,), right: (down,), left: (up,)},
    "-": {down: (left, right), up: (left, right), right: (right,), left: (left,)},
    "|": {down: (down,), up: (up,), right: (up, down), left: (up, down)},
    ".": {down: (down,), up: (up,), right: (right,), left: (left,)},
}


def propagate_beam(layout: list, start_configuration: tuple = None) -> int:
    height = len(layout)
    width = len(layout[0])
    beams = [start_configuration]
    energized_tiles = set()

    while beams:
        coord, direction = beams.pop(0)
        energized_tiles.add((coord, direction))

        for d in reflections[layout[coord[1]][coord[0]]][direction]:
            next_coord = coord + directions[d]
            if (next_coord, d) not in energized_tiles and (
                0 <= next_coord[1] < height and 0 <= next_coord[0] < width
            ):
                beams.append((next_coord, d))

    return len(set(c for c, _ in energized_tiles))


with open("./input", "r") as f:
    data = f.read().strip().splitlines()

# part 1:
print(propagate_beam(data, (Coord((0, 0)), right)))

# part 2
print(max(map(lambda config_gen: propagate_beam(data, start_configuration=config_gen),
              chain(((Coord((x, 0)), down) for x in range(len(data[0]))),
                    ((Coord((x, len(data) - 1)), up) for x in range(len(data[0]))),
                    ((Coord((0, y)), right) for y in range(len(data))),
                    ((Coord((len(data[0]) - 1, y)), left) for y in range(len(data)))))))
