#!/usr/bin/python
"""Advent of Code 2023, Day 15, Part 1

https://adventofcode.com/2023/day/15

Given a list of strings, calculate the hash value using the given algorithm and
total it up.

See test.dat for sample data and sequence.dat for full data.

Author: Tim Behrendsen
"""

import re
import sys

fn = 'test.dat'
fn = 'sequence.dat'

#
# Calculate hash code according to puzzle algorithm
#
def calc_hash(s):
    val = 0
    for c in s:
        val += ord(c)
        val *= 17
        val = val % 256

    return val

#
# Main processing.
#
def main():
    # Read in all the maps, each as an array of strings
    total = 0
    with open(fn, 'r') as file:
        seq = file.readline()
        seq = seq.rstrip('\n')

    total = 0
    s_list = seq.split(',')
    for s in s_list:
        hash_num = calc_hash(s)
        total += hash_num

    return total

total = main()
print(f"Total of hash numbers is {total}")
