#!/usr/bin/python
"""Advent of Code 2023, Day 15, Part 1

https://adventofcode.com/2023/day/15

For part 1, given a list of strings, calculate the hash value using the given
algorithm and total it up.

For part 2, the strings are a list of lens tags and lens numbers. Apply the operation
code (- or =) to place each one in a set of boxes, each of which may contains multiple
lenses.  Process each command, then total up the "focusing power" based on their box
numbers and lens numbers.

See test.dat for sample data and sequence.dat for full data.

Author: Tim Behrendsen
"""

import re
from functools import reduce

fn = 'test.dat'
fn = 'sequence.dat'

# Calculate hash code according to puzzle algorithm
def calc_hash(s):
    return reduce(lambda h, c: ((h + ord(c)) * 17) % 256, (c for c in s), 0)

def part1(s_list):
    return sum(calc_hash(s) for s in s_list)

def part2(s_list):
    boxes = [ [] for _ in range(256) ]

    # Find label within a box
    def find(box, label):
        return next((idx for idx in range(len(boxes[box])-1, -1, -1) if boxes[box][idx][0] == label), None)

    for s in s_list:
        label, op, lens = re.findall(r'(\w+)(-|=)(\d*)', s)[0]
        box = calc_hash(label)
        idx = find(box, label)

        if op == '-':
            # Remove lens, if exists
            if idx != None:
                del boxes[box][idx]

        else:       # op is '=': Add or replace lens in box
            if idx != None:
                boxes[box][idx] = (label, lens)         # Replace
            else:
                boxes[box].append((label, lens))        # Add new

    # Add up "focusing power" using formula
    return sum((box_num+1) * (slot+1) * int(lens[1])
        for box_num, box in enumerate(boxes) for slot, lens in enumerate(box))

s_list = open(fn, 'r').readline().rstrip().split(',')
print(f"Total of hash numbers is {part1(s_list)}")
print(f"Total of hash numbers is {part2(s_list)}")
