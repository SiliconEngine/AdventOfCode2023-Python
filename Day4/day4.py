#!/usr/bin/python
"""Advent of Code 2023, Day 4

https://adventofcode.com/2023/day/4

Part 1: Calculate score of scratcher tickets and total them up.

Part 2: Add up total number of scratcher cards, taking into account copying based
on the number of matching numbers of the prior cards.

See test.dat for sample data and cards.dat for full data.

Author: Tim Behrendsen
"""

import re

fn = 'cards.dat'

# Parse cards and generate a data structure
def gen_cards():
    for line in (line.strip() for line in open(fn, 'r')):
        matches = re.findall(r'Card\s+(\d+): (.*) \| (.*)', line)[0]
        winning = re.findall(r'\d+', matches[1])
        chosen = re.findall(r'\d+', matches[2])
        yield { 'num': matches[0], 'winning': winning, 'chosen': chosen }

# Calculate number of matching numbers
def count_matches(card):
    return sum(chosen in card['winning'] for chosen in card['chosen'])

# Calculate score of a card, 1 for one match, then doubling with each successive match.
def calc_score(card):
    n = count_matches(card)
    return 0 if n == 0 else 2**(n-1)

# Read cards and total up score
def part1():
    return sum(calc_score(card) for card in gen_cards())

def part2():
    # Read cards and create array of number of matches of each
    count_array = [count_matches(card) for card in gen_cards()]

    # Calculate the number of copies of each card
    copies = [1] * len(count_array)
    for idx, count in enumerate(count_array):
        cur_copies = copies[idx]
        for idx2 in range(idx+1, min(idx+count+1, len(count_array))):
            copies[idx2] += cur_copies

    # Calculate total number of cards and copies
    return sum(copies)

print(f"Total of cards is {part1()} points")
print(f"Total number of cards is {part2()}")
