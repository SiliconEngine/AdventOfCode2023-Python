#!/usr/bin/python
"""Advent of Code 2023, Day 13, Part 1

https://adventofcode.com/2023/day/13

Given a grid of '.' and '#' characters, find the reflection point that might be
vertical or horizontal. Total up the reflection rows / columns according to a formula.

See test.dat for sample data and image.dat for full data.

Author: Tim Behrendsen
"""

import re
import sys

fn = 'test.dat'
fn = 'maps.dat'


#
# Given a list of strings, rotate char grid 90 degrees
#
def rotate_map(cur_map):
    # Python trickery for rotating a list of strings
    rotated = [''.join(row) for row in zip(*cur_map[::-1])]
    return rotated

#
# Check for a vertical reflection among lines
#
def check_ref(cur_map):
    # Test each number as a mid-point
    for mid in range(0, len(cur_map)-1):
        no_match = False
        for offset in range(0, len(cur_map)-mid-1):
            idx1 = mid-offset
            idx2 = mid+offset+1

            # If hit top, then was good
            if idx1 < 0:
                return mid

            if cur_map[idx1] != cur_map[idx2]:
                no_match = True
                break

        if (not no_match):
            return mid

    return None

#
# Main processing. Read maps and calculate answer.
#
def main():
    # Read in all the maps, each as an array of strings
    total = 0
    with open(fn, 'r') as file:
        map_list = []
        cur_map = []
        while True:
            line = file.readline()
            if (line == '' or line == '\n'):
                if len(cur_map):
                    map_list.append(cur_map)
                    cur_map = []
                if (line == '\n'):
                    continue
                break

            line = line.rstrip('\n')
            cur_map.append(line)

    # Figure out any row / column reflections and calculate summary answer
    total = 0
    bad_count = 0
    map_num = 0
    for cur_map in map_list:
        map_num += 1

        # First check row reflection
        row = check_ref(cur_map)
        if row != None:
            total += 100 * (row + 1)

        # Second check column reflection
        flipped_map = rotate_map(cur_map)
        col = check_ref(flipped_map)
        if col != None:
            total += (col + 1)

        if row == None and col == None:
            bad_count += 1
            print(f"BOTH BAD #{bad_count}")
            exit(0)

        if row != None and col != None:
            print("BOTH GOOD")
            exit(0)

    return total

total = main()
print(f"Total summary number is {total}")
