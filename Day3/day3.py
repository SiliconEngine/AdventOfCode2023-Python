#!/usr/bin/python
"""Advent of Code 2023, Day 3

https://adventofcode.com/2023/day/3

Read "schematic" grid of numbers and symbols. In part 1, add up any numbers (sequence of
digits) that are adjacent to a non-period symbol, including diagonally.

In part 2, asterisk symbols are "gears". For any gears that are adjacent to exactly two
numbers, including diagonally, multiple the numbers together to give a "gear ratio". Sum
these numbers together.

See test.dat for sample data and schematic.dat for full data.

Author: Tim Behrendsen
"""

import re
fn = 'schematic.dat'

# Build list of parts
def get_part_list(schematic):
    part_list = []
    for row, line in enumerate(schematic):
        for match in re.finditer(r'\d+', line):
            start_pos, end_pos, num = match.start(), match.end()-1, match.group()
            part_list.append({ 'row': row, 'start_pos': start_pos, 'end_pos': end_pos, 'num': int(num) })
    return part_list

def part1(schematic):
    def has_sym(part):
        for chk_row in range(max(0, part['row']-1), min(num_rows-1, part['row']+1) + 1):
            for chk_col in range(max(0, part['start_pos']-1), min(num_cols-1, part['end_pos']+1) + 1):
                chk_c = schematic[chk_row][chk_col] 
                if chk_c != '.' and not chk_c.isdigit():
                    return True
        return False

    return sum(part['num'] for part in get_part_list(schematic) if has_sym(part))

def part2(schematic):
    part_list = get_part_list(schematic)

    # Scan for gears ('*') then see if it's adjacent to exactly two part numbers.
    total = 0
    for row, line in enumerate(schematic):
        for match in re.finditer(r'\*', line):
            col = match.start()
            match_parts = [ part for part in part_list
                if abs(row - part['row']) <= 1
                    and (part['start_pos']-1) <= col <= (part['end_pos']+1) ]

            # If valid, calculate the gear ratio and sum them up.
            if len(match_parts) == 2:
                total += match_parts[0]['num'] * match_parts[1]['num']

    return total

schematic = [ line.strip() for line in open(fn, 'r') ]
num_rows, num_cols = len(schematic), len(schematic[0])

print(f"Part number total is {part1(schematic)}")
print(f"Sum of all gear ratios is {part2(schematic)}")
