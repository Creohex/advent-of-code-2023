steps = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}
"""Discrete grid movement directions."""

connectors = {
    "-": [steps["left"], steps["right"]],
    "|": [steps["up"], steps["down"]],
    "L": [steps["up"], steps["right"]],
    "J": [steps["up"], steps["left"]],
    "7": [steps["down"], steps["left"]],
    "F": [steps["down"], steps["right"]],
}
"""Pipe segments and directions they connect."""

possible_connections = {
    steps["up"]: "|7F",
    steps["down"]: "|LJ",
    steps["left"]: "-LF",
    steps["right"]: "-J7",
}
"""Mapping of direction and types of pipe segments that can be connected to it."""

side_map = {
    "|": (steps["up"], [steps["right"]], [steps["left"]]),
    "-": (steps["left"], [steps["up"]], [steps["down"]]),
    "L": (steps["up"], [], [steps["left"], steps["down"]]),
    "J": (steps["left"], [], [steps["down"], steps["left"]]),
    "7": (steps["left"], [steps["up"], steps["right"]], []),
    "F": (steps["right"], [], [steps["left"], steps["up"]]),
}
"""Left/Right coord offsets depending on segment type and movement direction."""


def visualize(
    pipe_map: list,
    path: list = None,
    current_pos: tuple = None,
    inner: list = None,
    outer: list = None,
):
    m = list(map(list, pipe_map))
    for sign, coords in {
        "#": path or [],
        "I": inner or [],
        "O": outer or [],
        "*": current_pos or [],
    }.items():
        for x, y in coords:
            try:
                m[y][x] = sign
            except IndexError:
                pass
    list(map(lambda _: print("".join(_)), m + ["-" * 12]))


def explore_loop(pipe_map: list) -> list:
    def find_start() -> tuple:
        for y in range(len(pipe_map)):
            for x in range(len(pipe_map[0])):
                if pipe_map[y][x] == "S":
                    return x, y

    def connections(x: int, y: int) -> tuple:
        coords = []
        for (dx, dy), pipe_sign in possible_connections.items():
            neighbour_x, neighbour_y = x + dx, y + dy
            if pipe_map[neighbour_y][neighbour_x] in pipe_sign:
                coords.append((neighbour_x, neighbour_y))
        return coords

    def next_pipe(current: tuple, previous: tuple) -> tuple:
        x, y = current
        next_coords = connectors[pipe_map[y][x]]
        dx, dy = next_coords[
            0 if previous == (x + next_coords[1][0], y + next_coords[1][1]) else 1
        ]
        return x + dx, y + dy

    start = find_start()
    path = [start, connections(*start)[0]]

    while (hop := next_pipe(path[-1], path[-2])) != start:
        path.append(hop)

    return path


def find_enclosed_tiles(pipe_map: list, main_loop: list) -> int:
    l = set()
    r = set()

    def get_side_offsets(current: tuple, previous: tuple) -> tuple:
        segment = pipe_map[current[1]][current[0]]
        dx = previous[0] - current[0]
        dy = previous[1] - current[1]
        direction, l, r = side_map[segment]
        return (l, r) if direction == (dx, dy) else (r, l)

    for i in range(len(main_loop) - 1):
        previous = main_loop[i]
        current = main_loop[i + 1]

        l_offsets, r_offsets = get_side_offsets(current, previous)
        for l_offset in l_offsets:
            l_coord = (current[0] + l_offset[0], current[1] + l_offset[1])
            if l_coord not in main_loop:
                l.add(l_coord)
        for r_offset in r_offsets:
            r_coord = (current[0] + r_offset[0], current[1] + r_offset[1])
            if r_coord not in main_loop:
                r.add(r_coord)

    def expand_areas(coords: set) -> None:
        investigated = set()
        to_investigate = set(coords)
        while to_investigate:
            current = to_investigate.pop()
            for dx, dy in steps.values():
                neighbour = current[0] + dx, current[1] + dy
                if neighbour not in main_loop and neighbour not in investigated:
                    coords.add(neighbour)
                    to_investigate.add(neighbour)
            investigated.add(current)

    # decide which set is inner (lazy version)
    l, r = (l, r) if len(l) <= len(r) else (r, l)

    expand_areas(l)
    visualize(pipe_map, path=main_loop, inner=l, outer=r)

    return l


with open("./input", "r") as f:
    pipes = f.read().strip().splitlines()
loop = explore_loop(pipes)
enclosed = find_enclosed_tiles(pipes, loop)
print(f"Part 1: {len(loop) // 2}")
print(f"Part 2: {len(enclosed)}")
