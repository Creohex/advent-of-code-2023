#!python

def count_points(cards):
    points = 0
    for winning, actual in cards:
        amount = len(winning.intersection(actual))
        points += 1 if amount == 1 else 2 ** (amount - 1) if amount > 1 else 0
    return points

def count_compounding_cards(cards):
    cards_in_play = [1 for _ in cards]
    for i, (winning, actual) in enumerate(cards):
        amount_won = len(winning.intersection(actual))
        if amount_won:
            for di in range(i + 1, i + 1 + amount_won):
                cards_in_play[di] += cards_in_play[i]
    return sum(cards_in_play)


with open("./input", "r") as f:
    cards = [tuple(map(set, map(lambda c: c.strip().split(),
                                card.split(":")[1].split("|"))))
            for card in f.readlines()]

# part 1:
print(count_points(cards))

# part 2:
print(count_compounding_cards(cards))
