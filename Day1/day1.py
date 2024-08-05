#!/usr/bin/python
"""Advent of Code 2023, Day 1

https://adventofcode.com/2023/day/1

Read lines, find first digit and last digit, combine to a number, and total. See
test.dat for sample data and calibrate.dat for full data.

For part 2, a digit may be spelled out, except for 'zero'. The tricky part was
that you could have overlap, like "eighthree" should be 83, so had to use regex lookahead.

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

def get_total(lines, part):
    total = 0
    for line in lines:
        if part == 1:
            matches = re.findall(r'\d', line)
            first = matches[0]
            last = matches[-1]
        else:
            matches = re.findall(r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))', line)
            first = tran.get(matches[0], matches[0])
            last = tran.get(matches[-1], matches[-1])

        total += int(first + last)

    return total

lines = [ line.strip() for line in open(fn, 'r') ]
print(f"Part 1 is {get_total(lines, part=1)}")
print(f"Part 2 is {get_total(lines, part=2)}")
