#!python


class Coord(tuple):
    def __add__(self, other):
        return Coord(a + b for a, b in zip(self, other))
    def __sub__(self, other):
        return Coord(a - b for a, b in zip(self, other))
    def __mul__(self, mul_by):
        return Coord(a * mul_by for a in self)


def parse_input(source: list, instructions_from_color: bool = False) -> list:
    if instructions_from_color:
        return list(map(lambda c: ("RDLU"[int(c[-1])], int(c[:-1], 16)),
                        (color.strip("(#)") for _, _, color in map(str.split, source))))
    return [(dir, int(steps)) for dir, steps, _ in map(str.split, source)]


def shoelace(vertices: list) -> int:
    area = 0.0
    for i in range(len(vertices)):
        j = (i + 1) % len(vertices)
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[j][0] * vertices[i][1]
    return int(abs(area) // 2)


def boundary_points(grid: list) -> int:
    ans = 0
    for i in range(len(grid) - 1):
        diff = grid[i + 1] - grid[i]
        ans += abs(sum(diff))
    return ans


def dig(instructions: list) -> int:
    directions = {
        "R": Coord((0, 1)),
        "D": Coord((1, 0)),
        "L": Coord((0, -1)),
        "U": Coord((-1, 0)),
    }
    grid = [Coord((0, 0))]

    for direction, steps in instructions:
        grid.append(grid[-1] + directions[direction] * steps)

    return shoelace(grid) + boundary_points(grid) // 2 + 1


with open("./input", "r") as f:
    data = f.readlines()

# Part 1:
print(dig(parse_input(data)))

# Part 2:
print(dig(parse_input(data, instructions_from_color=True)))
