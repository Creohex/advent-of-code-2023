#!python

import re
from functools import reduce


hash_func = lambda text: reduce(lambda acc, c: (acc + ord(c)) * 17 % 256, text, 0)


def organize_lenses(manual: str):
    pattern = r"(\w+)(?:-|=(\d))"
    boxes = {_: [] for _ in range(256)}
    focal_lengths = {}

    for record in records:
        lens_label, focal_length = re.findall(pattern, record).pop()
        box_number = hash_func(lens_label)

        if focal_length:
            focal_length = int(focal_length)
            focal_lengths[lens_label] = focal_length
            if lens_label not in boxes[box_number]:
                boxes[box_number].append(lens_label)
        else:
            if lens_label in boxes[box_number]:
                boxes[box_number].pop(boxes[box_number].index(lens_label))

    return sum(
        (box + 1) * i * focal_lengths[lens]
        for box, lenses in boxes.items()
        for i, lens in enumerate(lenses, 1)
    )


with open("./input", "r") as f:
    records = f.read().strip().split(",")

# part 1:
print(sum(map(hash_func, records)))

# part 2:
print(organize_lenses(records))
