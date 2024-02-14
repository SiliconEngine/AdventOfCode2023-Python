#!/usr/bin/python
"""Advent of Code 2023, Day 4, Part 1

https://adventofcode.com/2023/day/4

Calculate score of scratcher tickets and total them up.
See test.dat for sample data and cards.dat for full data.

Author: Tim Behrendsen
"""

import re

fn = 'cards.dat'

# Calculate score of a card, 1 for one match, then doubling with each successive match.
def calc_score(card):
    score = 0
    for chosen in card['chosen']:
        if (chosen in card['winning']):
            score = 1 if score == 0 else score * 2
    return score

# Read cards and total up score
total = 0

with open(fn, 'r') as file:
    for line in file:
        line = line.rstrip('\n')

        matches = re.findall(r'Card\s+(\d+): (.*) \| (.*)', line)
        winning = re.findall(r'\d+', matches[0][1])
        chosen = re.findall(r'\d+', matches[0][2])

        card = { 'num': matches[0][0], 'winning': winning, 'chosen': chosen }

        score = calc_score(card)
        total += score

print(f"Total of cards is {total} points")
