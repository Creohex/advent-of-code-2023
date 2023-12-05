#!python

import re
from functools import reduce


with open("./input", "r") as file:
    rounds = file.readlines()

dice_limits = {
    "red": 12,
    "green": 13,
    "blue": 14,
}
combination_pattern = r"(\d+) (red|green|blue)"


def play_round(round):
    header, dice_sets = round.split(":")
    for dice_set in dice_sets.split(";"):
        for amount, color in re.findall(combination_pattern, dice_set):
            if int(amount) > dice_limits[color]:
                return 0
    return int(re.search(r"\d+", header).group())


def play_round_fewest_cubes(round):
    _, dice_sets = round.split(":")
    dice = {}
    for dice_set in dice_sets.split(";"):
        for amount, color in re.findall(combination_pattern, dice_set):
            dice[color] = max(dice.get(color, 0), int(amount))
    return reduce(lambda a, b: a * b, dice.values())


# part 1
print(sum(map(play_round, rounds)))

# part 2
print(sum(map(play_round_fewest_cubes, rounds)))
