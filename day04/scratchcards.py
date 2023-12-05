#!python

import re


def count_points(cards):
    points = 0
    for winning, actual in cards:
        amount = len(winning.intersection(actual))
        if amount == 1:
            points += 1
        elif amount > 1:
            points += 2 ** (amount - 1)
    return points

def count_compounding_cards(cards):
    cards_in_play = [1 for _ in range(len(cards))]

    for i, (winning, actual) in enumerate(cards):
        amount_won = len(winning.intersection(actual))
        if amount_won:
            for di in range(i + 1, i + 1 + amount_won):
                cards_in_play[di] += cards_in_play[i]

    return sum(cards_in_play)


with open("./input", "r") as f:
    cards = [tuple(map(set, map(lambda c: re.findall(r"\d+", c),
                                card.split(":")[1].split("|"))))
            for card in f.readlines()]

# part 1:
print(count_points(cards))

# part 2:
print(count_compounding_cards(cards))
