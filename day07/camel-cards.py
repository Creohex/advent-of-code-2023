#!python

from dataclasses import dataclass

@dataclass
class Hand:
    cards: str
    bid: int

    def weight(self, jacks_are_jokers=False):
        card_order = "J23456789TQKA" if jacks_are_jokers else "23456789TJQKA"
        cards = {c: self.cards.count(c) for c in set(self.cards)}
        if jacks_are_jokers:
            jockers = cards.pop("J", 0)
            if cards:
                max_cards = max(cards.values())
                jocker_type = max(filter(lambda card: cards[card] == max_cards, cards),
                                  key=lambda c_type: card_order.index(c_type))
                cards[jocker_type] += jockers
            else:
                cards[card_order[-1]] = jockers
        cards_value = -int("".join(map(str, sorted(cards.values())))) * 1000000
        order_value = sum((13 ** (5 - i)) * card_order.index(c) for i, c in enumerate(self.cards))

        return cards_value + order_value


with open("./input", "r") as f:
    hands = [Hand(cards, int(bid)) for cards, bid in map(str.split, f.readlines())]

# part 1:
print(sum(hand.bid * rank for rank, hand
          in enumerate(sorted(hands, key=lambda h: h.weight()), start=1)))

# part 2:
print(sum(hand.bid * rank for rank, hand
          in enumerate(sorted(hands, key=lambda h: h.weight(jacks_are_jokers=True)), start=1)))
