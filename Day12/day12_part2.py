#!/usr/bin/python
"""Advent of Code 2023, Day 12, Part 2

https://adventofcode.com/2023/day/12

Given a pattern with missing information, figure out the number of combinations
that could potentially fit the set of numbers given (set of number of hashes in a row).
For part 2, the pattern is repeated four more times.

Because the patterns are much larger, brute-force becomes impractical. This algorithm
uses dynamic programming to cache parts of patterns so we can reuse that information
when we see common patterns.

See test.dat for sample data and image.dat for full data.

Author: Tim Behrendsen
"""

import re
import sys
from functools import reduce
from operator import add

fn = 'test.dat'
fn = 'records.dat'

# Cache for storing visited patterns to memoize
cache = {}

#
# Check if pattern is consistent with the hash counts
# Returns tuple of:
#         True/false, if done
#         Count of number of pattern matches
#
def chk_done(springs, counts):
    def get_count(chk_list, counts):
        same_count = 0
        for idx in range(min(len(chk_list), len(counts))):
            if chk_list[idx] != counts[idx]:
                break
            same_count += 1
        return same_count

    chk_list = []
    hash_count = 0
    had_q = False
    for c in springs:
        if c == ord('?'):
            #return (False, get_count(chk_list, counts))
            hash_count = 0
            had_q = True
            break
        elif c == ord('#'):
            hash_count += 1
        elif hash_count > 0:
            chk_list.append(hash_count)
            hash_count = 0
    
    if hash_count > 0:
        chk_list.append(hash_count)

    return (not had_q and counts == chk_list, get_count(chk_list, counts))

#
# Check if pattern we're testing is possible, so we can trim that part of the tree
#
def check_if_possible(springs, counts):
    chk_list = []
    hash_count = 0
    for c in springs:
        if c == ord('?'):
            hash_count = 0
            break

        elif c == ord('#'):
            hash_count += 1

        # Must be '.'
        elif hash_count > 0:
            chk_list.append(hash_count)
            hash_count = 0
    
    if hash_count > 0:
        chk_list.append(hash_count)

    is_possible = len(chk_list) == 0 or chk_list == counts[0:len(chk_list)]
    if not is_possible:
        return is_possible

    # If perfect match, we're good
    if chk_list == counts:
        return True

    num_needed = reduce(add, counts)
    num_have = 0
    hit_q = False
    for c in springs:
        if c == ord('?') or c == ord('#'):
            num_have += 1

    return num_have >= num_needed

#
# Create key for the pattern cache
#
def get_key(chk_count, springs, idx):
    return f"{chk_count}-{springs[idx:].decode('ascii')}"

#
# Recursively test each pattern
# Returns total number of patterns, totallying up each recursive call
#
def do_combos(springs, counts):
    total = 0
    try:
        if not check_if_possible(springs, counts):
            return 0

        (is_done, chk_count) = chk_done(springs, counts)
        if is_done:
            return 1

        idx = springs.index(ord('?'))
        key = get_key(chk_count, springs, idx)

        if idx > 0 and springs[idx-1] == ord('.'):
            cache_total = cache.get(key)
            if cache_total != None:
                return cache_total

        # Try '.'
        springs[idx] = ord('.')
        total += do_combos(springs, counts)

        # Try '#'
        springs[idx] = ord('#')
        total += do_combos(springs, counts)

        # Restore ?
        springs[idx] = ord('?')

        # Store cache of chk_count and rest of string
        if idx > 0 and springs[idx-1] == ord('.'):
            cache[key] = total

        return total

    except ValueError:
        # No more unknowns, if consistent count this, otherwise don't
        (is_done, chk_count) = chk_done(springs, counts)
        return 1 if is_done else 0

    return total

#
# Figure out number of combinations for 'springs' pattern and counts
# of hashes
#
# Returns number of patterns
#
def calc_combos(springs, counts):
    # Reset the cache
    global cache
    cache = {}

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

            # Get the pattern and counts, and repeat four more times
            a = line.split(' ')
            springs = a[0] + '?' + a[0] + '?' + a[0] + '?' + a[0] + '?' + a[0]
            counts = [ int(n) for n in a[1].split(',') ]
            counts = counts + counts + counts + counts + counts

            num = calc_combos(springs, counts)
            print(f"---> num is {num}\n")
            total += num

    return total

total = main()
print(f"Total combinations is {total}")
