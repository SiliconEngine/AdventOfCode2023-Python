#!/usr/bin/python
"""Advent of Code 2023, Day 3, Part 2

https://adventofcode.com/2023/day/3

Read "schematic" grid of numbers and symbols. Asterisk symbols are "gears". For
any gears that are adjacent to exactly two numbers, including diagonally,
multiple the numbers together to give a "gear ratio". Sum these numbers together.

See test.dat for sample data and schematic.dat for full data.

Author: Tim Behrendsen
"""

import re

fn = 'schematic.dat'

total = 0
schematic = []
num_rows = 0
num_cols = 0

with open(fn, 'r') as file:
    for line in file:
        line = line.rstrip('\n')
        schematic.append(line)

num_rows = len(schematic)
num_cols = len(schematic[0])

total = 0

# First build list of all part numbers
part_list = []
row = 0
for line in schematic:
    matches = re.finditer(r'\d+', line)
    for match in matches:
        start_pos = match.start()
        end_pos = match.end()-1
        num = match.group()
        part_list.append({ 'row': row, 'start_pos': start_pos, 'end_pos': end_pos, 'num': int(num) })

    row += 1

# Scan for gears ('*') then see if it's adjacent to exactly two part numbers.
row = 0
for line in schematic:
    matches = re.finditer(r'\*', line)
    for match in matches:
        col = match.start()
        match_parts = []
        for part in part_list:
            if (abs(row - part['row']) <= 1 and col >= (part['start_pos']-1) and col <= (part['end_pos']+1)):
                match_parts.append(part)

        # If valid, calculate the gear ratio and sum them up.
        if (len(match_parts) == 2):
            total += match_parts[0]['num'] * match_parts[1]['num']

    row += 1

print(f"Sum of all gear ratios is {total}")
