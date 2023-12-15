#!python


def turn_image(image: list) -> list:
    return ["".join(image[x][y] for x in range(len(image))) for y in range(len(image[0]))]


def line_symmetries(line: str) -> set:
    symmetry_indices = set()
    for i in range(1, len(line)):
        width = min(i, len(line) - i)
        l, r = line[abs(i - width) : i], line[i : i + i]
        if l == r[::-1]:
            symmetry_indices.add(i)
    return symmetry_indices


def vertical_symmetry(image: list) -> list:
    axis = dict()
    for symmetries in map(line_symmetries, image):
        for s in symmetries:
            axis[s] = axis.get(s, 0) + 1
    return tuple(
        next((k for k, v in axis.items() if v == i), None)
        for i in (len(image), len(image) - 1)
    )


def symmetries(image: list) -> tuple:
    v, v_smudge = vertical_symmetry(image)
    h, h_smudge = vertical_symmetry(turn_image(image))
    return (v or 100 * h), (v_smudge or 100 * h_smudge)


with open("./input", "r") as f:
    images = map(str.split, f.read().split("\n\n"))

symmetry_values = list(map(symmetries, images))
print(f"Part 1: {sum(full_symmetry for full_symmetry, _ in symmetry_values)}")
print(f"Part 2: {sum(smudge_symmetries for _, smudge_symmetries in symmetry_values)}")
