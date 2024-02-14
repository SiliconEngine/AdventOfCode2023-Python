#!/usr/bin/python
"""Advent of Code 2023, Day 3, Part 1

https://adventofcode.com/2023/day/3

Read "schematic" grid of numbers and symbols. Add up any numbers (sequence of
digits) that are adjacent to a non-period symbol, including diagonally.

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
row = 0

for line in schematic:
    matches = re.finditer(r'\d+', line)
    for match in matches:
        start_pos = match.start()
        end_pos = match.end()-1
        num = match.group()

        has_sym = False
        for chk_row in range(max(0, row-1), min(num_rows-1, row+1) + 1):
            for chk_col in range(max(0, start_pos-1), min(num_cols-1, end_pos+1) + 1):
                chk_c = schematic[chk_row][chk_col] 
                if (not (chk_c == '.' or (chk_c >= '0' and chk_c <= '9'))):
                    has_sym = True
                    break
            if (has_sym):
                break

        if (has_sym):
            total += int(num)

    row += 1

print(f"Part number total is {total}")
