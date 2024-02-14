#!/usr/bin/python
"""Advent of Code 2023, Day 4, Part 2

https://adventofcode.com/2023/day/4

Add up total number of scratcher cards, taking into account copying based
on the number of matching numbers of the prior cards.

See test.dat for sample data and cards.dat for full data.

Author: Tim Behrendsen
"""

import re

fn = 'cards.dat'

# Calculate number of matching numbers
def calc_matches(card):
    count = 0
    for chosen in card['chosen']:
        if (chosen in card['winning']):
            count += 1
    return count


# Read cards and create array of number of matches of each
count_array = []
copies = []

with open(fn, 'r') as file:
    for line in file:
        line = line.rstrip('\n')

        matches = re.findall(r'Card\s+(\d+): (.*) \| (.*)', line)
        winning = re.findall(r'\d+', matches[0][1])
        chosen = re.findall(r'\d+', matches[0][2])
        card = { 'num': matches[0][0], 'winning': winning, 'chosen': chosen }

        count = calc_matches(card)
        count_array.append(count)
        copies.append(1)

# Calculate the number of copies of each card
for idx in range(0, len(count_array)):
    count = count_array[idx]
    cur_copies = copies[idx]
    for idx2 in range(idx+1, min(idx+count+1, len(count_array))):
        copies[idx2] += cur_copies

# Calculate total number of cards and copies
num_cards = 0
for idx in range(0, len(count_array)):
    num_cards += copies[idx]

print(f"Total number of cards is {num_cards}")
