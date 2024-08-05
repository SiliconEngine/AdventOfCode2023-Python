#!/usr/bin/python
"""Advent of Code 2023, Day 7

https://adventofcode.com/2023/day/7

Give sets of five playing cards, figure the hand type and rank them by strength.
Finally calculate a winning score by multiplying the bid by the index. In part 2,
the 'J' is now a joker, instead of a jack.

If hands are equal type, then cards are compared in order to determine which hand
is the strongest.

See test.dat for sample data and cards.dat for full data.

Author: Tim Behrendsen
"""

import re
from enum import Enum
from functools import cmp_to_key

fn = 'test.dat'
fn = 'cards.dat'

Hand = Enum('Hand', 'FIVE_KIND FOUR_KIND FULL_HOUSE THREE_KIND TWO_PAIR ONE_PAIR HIGH_CARD')

#
# Figure hand type and return Hand enum type
#
def get_hand_type(hand, jokers):
    class Counts:
        def __init__(self, card, count):
            self.card, self.count = card, count

    counts = { }
    for card in hand:
        counts[card] = counts.get(card, 0) + 1

    num_jokers = 0
    if jokers:
        num_jokers = counts.get('J', 0)
        counts.pop('J', None)
        if num_jokers == 5:
            return Hand.FIVE_KIND

    list = [Counts(k, v) for k, v in counts.items() ]
    list.sort(key=lambda e: e.count, reverse=True)

    if list[0].count == 5 or list[0].count + num_jokers == 5:
        return Hand.FIVE_KIND

    if list[0].count == 4 or list[0].count + num_jokers == 4:
        return Hand.FOUR_KIND

    if list[0].count == 3 and list[1].count == 2:
        return Hand.FULL_HOUSE

    if (list[0].count + num_jokers) == 3 and list[1].count == 2:
        return Hand.FULL_HOUSE

    # I think this one is impossible, would be four-of-a-kind
    if list[0].count == 3 and (list[1].count + num_jokers) == 2:
        return Hand.FULL_HOUSE

    if list[0].count == 3 or (list[0].count + num_jokers) == 3:
        return Hand.THREE_KIND

    # Also covers the case of no jokers. I think two-pair with jokers is impossible.
    if list[0].count == 2 and (list[1].count + num_jokers) == 2:
        return Hand.TWO_PAIR

    # Also covers the case of no jokers
    if (list[0].count + num_jokers) == 2:
        return Hand.ONE_PAIR

    return Hand.HIGH_CARD

# Calculate winnings, depending on whether Jacks are actually Jokers
def calc(hand_list, jokers):
    # Card rank varies whether it has Jokers or Jacks
    card_ranks = '123456789TJQKA' if not jokers else 'J123456789TQKA'

    for hand in hand_list:
        hand['type'] = get_hand_type(hand['cards'], jokers)

    # Sort hands by strength
    # Sort by hand strength, then by each card in order
    sort_order = lambda hand: [0-hand['type'].value] + [card_ranks.index(c) for c in hand['cards']]
    hand_list.sort(key=sort_order)

    # Calculate total winnings
    return sum(hand['bid'] * (i+1) for i, hand in enumerate(hand_list))

hand_list = [ { 'cards': cards, 'bid': int(bid) } for cards, bid in
    (re.findall(r'(\w{5}) (\d+)', line)[0] for line in open(fn, 'r')) ]

print(f"Part 1: total winnings is {calc(hand_list.copy(), jokers=False)}")
print(f"Part 2: total winnings is {calc(hand_list.copy(), jokers=True)}")

