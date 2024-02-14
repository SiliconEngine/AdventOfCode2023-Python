#!/usr/bin/python
"""Advent of Code 2023, Day 1, Part 1

https://adventofcode.com/2023/day/1

Read lines, find first digit and last digit, combine to a number, and total.
See test.dat for sample data and calibrate.dat for full data.

Author: Tim Behrendsen
"""

import re

fn = 'calibrate.dat'

with open(fn, 'r') as file:
    total = 0
    for line in file:
        line = line.rstrip('\n')
        matches = re.findall(r'\d', line)
        first = matches[0]
        last = matches[-1]
        number = int(first + last)
        total += number

print(f"Total = {total}")
