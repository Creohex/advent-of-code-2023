#!python

from functools import reduce

with open("./input", "r") as f:
    cards = list(map(lambda nums: reduce(lambda w, a: len(set(w).intersection(a)), nums),
                     map(lambda raw: (_.strip().split() for _
                                      in raw.split(":")[1].split("|")),
                         f.readlines())))

# part 1:
print(sum(1 if wins == 1 else 2 ** (wins - 1) if wins > 1 else 0 for wins in cards))

# part 2:
cards_in_play = [1] * len(cards)
for i, wins in enumerate(cards):
    for di in range(i + 1, i + 1 + wins):
        cards_in_play[di] += cards_in_play[i]
print(sum(cards_in_play))
