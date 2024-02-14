#!/usr/bin/python
"""Advent of Code 2023, Day 7, Part 1

https://adventofcode.com/2023/day/7

Give sets of five playing cards, figure the hand type and rank them by strength.
Finally calculate a winning score by multiplying the bid by the index.

See test.dat for sample data and cards.dat for full data.

Author: Tim Behrendsen
"""

import re
from enum import Enum
from functools import cmp_to_key

fn = 'test.dat'
fn = 'cards.dat'

Hand = Enum('Hand', 'FIVE_KIND FOUR_KIND FULL_HOUSE THREE_KIND TWO_PAIR ONE_PAIR HIGH_CARD')

card_ranks = '123456789TJQKA'

#
# Figure hand type and return Hand enum type
#
def get_hand_type(cards):
    class Counts:
        def __init__(self, card, count):
            self.card = card
            self.count = count
        
        def __repr__(self):
            return f"[{self.card} {self.count}]"

    counts = { }
    for card in cards:
        counts[card] = counts.get(card, 0) + 1

    list = [Counts(k, v) for k, v in counts.items() ]
    list.sort(key=lambda e: e.count, reverse=True)

    if list[0].count == 5:
        return Hand.FIVE_KIND

    if list[0].count == 4:
        return Hand.FOUR_KIND

    if list[0].count == 3 and list[1].count == 2:
        return Hand.FULL_HOUSE

    if list[0].count == 3:
        return Hand.THREE_KIND

    if list[0].count == 2 and list[1].count == 2:
        return Hand.TWO_PAIR

    if list[0].count == 2:
        return Hand.ONE_PAIR

    return Hand.HIGH_CARD

#
# Compare cards for sort
#
def compare_hands(a, b):
    n = b['type'].value - a['type'].value
    if (n != 0):
        return n

    # If equal value, then compare by card strength
    crd1 = a['cards']
    crd2 = b['cards']
    for i in range(5):
        c1 = crd1[i]
        c2 = crd2[i]
        if (c1 != c2):
            return card_ranks.index(c1) - card_ranks.index(c2)
    
    return 0

# Read card hands and build list with classification
card_list = []
with open(fn, 'r') as file:
    for line in file:
        matches = re.findall(r'(\w{5}) (\d+)', line)
        card_list.append({ 'cards': matches[0][0], 'bid': int(matches[0][1]), 'type': get_hand_type(matches[0][0]) })

# Sort hands by strength
card_list.sort(key=cmp_to_key(compare_hands))

# Calculate total winnings
winnings = 0
for i in range(len(card_list)):
    card = card_list[i]
    winnings += card['bid'] * (i+1)

print(f"Total winnings is {winnings}")
