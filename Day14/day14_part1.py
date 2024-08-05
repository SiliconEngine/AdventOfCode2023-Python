#!/usr/bin/python
"""Advent of Code 2023, Day 14, Part 1

https://adventofcode.com/2023/day/14

Given a grid of rocks, some rollable and some not, "tilt" the grid and roll the
rocks to the north. Afterward, calculate a "load number" using a formula.

See test.dat for sample data and platform.dat for full data.

Author: Tim Behrendsen
"""

import re
import sys

fn = 'test.dat'
fn = 'platform.dat'

round_rock = ord('O')
square_rock = ord('#')
space = ord('.')

def roll_north(platform):
    num_rows = len(platform)
    num_cols = len(platform[0])

    for col in range(0, num_cols):
        for row in range(1, num_rows):
            if platform[row][col] == round_rock:
                for chk_row in range(row-1, -2, -1):
                    if chk_row < 0 or platform[chk_row][col] != space:
                        platform[row][col] = space
                        platform[chk_row+1][col] = round_rock
                        break

def calc_north_load(platform):
    num_rows = len(platform)
    num_cols = len(platform[0])
    total_load = 0
    for row in range(num_rows):
        for col in range(num_cols):
            if (platform[row][col] == round_rock):
                total_load += (num_rows - row)

    return total_load

#
# Main processing. Read rock map and calculate answer.
#
def main():
    # Read in the grid of rocks
    total = 0
    with open(fn, 'r') as file:
        platform = []
        for line in file:
            line = line.rstrip('\n')
            platform.append(bytearray(line, encoding='ascii'))

    roll_north(platform)
    load = calc_north_load(platform)

    return load

load = main()
print(f"Total load number is {load}")
