#!/usr/bin/python
"""Advent of Code 2023, Day 12, Part 1

https://adventofcode.com/2023/day/12

Given a pattern with missing information, figure out the number of combinations
that could potentially fit the set of numbers given (set of number of hashes in
a row).

This part 1 solution uses simple brute-force recursion.

See test.dat for sample data and image.dat for full data.

Author: Tim Behrendsen
"""

import re
import sys

fn = 'test.dat'
fn = 'records.dat'

#
# Check if pattern is consistent with the hash counts
#
def chk_consist(springs, counts):
    chk_list = []
    hash_count = 0
    for c in springs:
        if (c == ord('#')):
            hash_count += 1
        elif hash_count > 0:
            chk_list.append(hash_count)
            hash_count = 0
    
    if hash_count > 0:
        chk_list.append(hash_count)

    return counts == chk_list


#
# Recursively test each pattern
# Returns total number of patterns, totallying up each recursive call
#
def do_combos(springs, counts):
    total = 0
    try:
        idx = springs.index(ord('?'))
        springs[idx] = ord('.')
        total += do_combos(springs, counts)
        springs[idx] = ord('#')
        total += do_combos(springs, counts)
        springs[idx] = ord('?')

    except ValueError:
        # No more unknowns, if consistent count this, otherwise don't
        return 1 if chk_consist(springs, counts) else 0

    return total

#
# Figure out number of combinations for 'springs' pattern and counts
# of hashes
#
# Returns number of patterns
#
def calc_combos(s):
    a = s.split(' ')
    springs = a[0]
    counts = [ int(n) for n in a[1].split(',') ]
    num = do_combos(bytearray(springs, encoding='ascii'), counts)
    return num


#
# Main processing. Return total number of pattern matches.
#
def main():
    # Read each spring map, calculate combos and total them up
    total = 0
    with open(fn, 'r') as file:
        for line in file:
            line = line.rstrip('\n')
            print(line)
            num = calc_combos(line)
            print(f"---> num is {num}\n")
            total += num

    return total

total = main()
print(f"Total combinations is {total}")
