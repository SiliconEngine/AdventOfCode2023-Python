#!/usr/bin/python
"""Advent of Code 2023, Day 1, Part 2

https://adventofcode.com/2023/day/1

Read lines, find first digit and last digit, combine to a number, and total. However, a digit
may be spelled out, except for 'zero'. The tricky part was that you could have overlap, like
"eighthree" should be 83, so had to use regex lookahead.

See test.dat for sample data and calibrate.dat for full data.

Author: Tim Behrendsen
"""

import re

fn = 'calibrate.dat'

tran = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

total = 0
with open(fn, 'r') as file:
    for line in file:
        line = line.rstrip('\n')
        matches = re.findall(r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))', line)

        first = matches[0]
        last = matches[-1]
        first = tran.get(first, first)
        last = tran.get(last, last)
        number = int(first + last)
        total += number

print(f"Total = {total}")
