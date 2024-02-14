#!/usr/bin/python
"""Advent of Code 2023, Day 14, Part 2

https://adventofcode.com/2023/day/14

Given a grid of rocks, some rollable and some not, "tilt" the grid in each of
four directions, and roll the rocks in that direction. Repeat the cycle
1,000,000,000 times and calculate the final "load number" using a formula.

Required noticing the load number falls into a repeating pattern, so figures
out the pattern and calculates the 1,000,000,000 based on the pattern length.

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

def print_plat(platform):
    for line in platform:
        print(line)

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

def roll_south(platform):
    num_rows = len(platform)
    num_cols = len(platform[0])

    for col in range(0, num_cols):
        for row in range(num_rows-2, -1, -1):
            if platform[row][col] == round_rock:
                for chk_row in range(row+1, num_rows+1):
                    if chk_row == num_rows or platform[chk_row][col] != space:
                        platform[row][col] = space
                        platform[chk_row-1][col] = round_rock
                        break

def roll_west(platform):
    num_rows = len(platform)
    num_cols = len(platform[0])

    for row in range(0, num_rows):
        for col in range(1, num_cols):
            if platform[row][col] == round_rock:
                for chk_col in range(col-1, -2, -1):
                    if chk_col < 0 or platform[row][chk_col] != space:
                        platform[row][col] = space
                        platform[row][chk_col+1] = round_rock
                        break

def roll_east(platform):
    num_rows = len(platform)
    num_cols = len(platform[0])

    for row in range(0, num_rows):
        for col in range(num_cols-2, -1, -1):
            if platform[row][col] == round_rock:
                for chk_col in range(col+1, num_cols+1):
                    if chk_col == num_cols or platform[row][chk_col] != space:
                        platform[row][col] = space
                        platform[row][chk_col-1] = round_rock
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

    cycles_to_calc = 1000000000

    # The nature of the problem is that the cycles will be cyclical after a
    # period to calm down. Run 100 cycles then figure out the repeating pattern.
    for cycle in range(100):
        roll_north(platform)
        roll_west(platform)
        roll_south(platform)
        roll_east(platform)

    # Get 50 more to check the pattern
    pattern = []
    for cycle in range(50):
        roll_north(platform)
        roll_west(platform)
        roll_south(platform)
        roll_east(platform)
        load = calc_north_load(platform)
        pattern.append(load)

    first_four = pattern[0:4]
    for idx in range(1, len(pattern)-3):
        if first_four == pattern[idx:idx+4]:
            cycle_len = idx
            break

    # Make sure the cycle repeats
    for idx in range(0, cycle_len):
        if pattern[idx] != pattern[idx+cycle_len]:
            raise Exception("Pattern check failed")

    # Based on the cycle length, use the modulo of the big number of cycles
    # to figure out where in the pattern that is
    offset = (cycles_to_calc - 100 - 1) % cycle_len
    load = pattern[offset]

    return load

load = main()
print(f"Total load number is {load}")
