#!python

from functools import reduce

test = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""


def find_symmetry(line):
    indices = set()
    print("---> ", line)
    for i in range(1, len(line)):
        width = min(i, len(line) - i)
        l, r = line[abs(i - width) : i], line[i : i + i]
        print(i, line[:i], line[i:], "|", l, r)
        if l == r[::-1]:
            indices.add(i)
    print("symmetry: ", indices)
    return indices


def turn_image(image):
    return ["".join(image[x][y] for x in range(len(image))) for y in range(len(image[0]))]


def solve(image):
    print("\n".join(image))

    axis = reduce(lambda a, b: a.intersection(b), map(find_symmetry, image))
    if axis:
        return axis.pop()

    if not axis:
        axis = reduce(lambda a, b: a.intersection(b), map(find_symmetry, turn_image(image)))
        return 100 * axis.pop()


with open("./input", "r") as f:
    images = f.read().split("\n\n")


# part 1:
print(sum(map(solve, map(str.splitlines, images))))
