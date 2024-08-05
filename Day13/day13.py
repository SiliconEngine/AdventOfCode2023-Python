#!/usr/bin/python
"""Advent of Code 2023, Day 13

https://adventofcode.com/2023/day/13

Given a grid of '.' and '#' characters, find the reflection point that might be
vertical or horizontal. Total up the reflection rows / columns according to a formula.

In Part 2, exactly one character must be switched to find new reflections. Total up
the reflection rows / columns according to a formula.

See test.dat for sample data and image.dat for full data.

Author: Tim Behrendsen
"""

fn = 'test.dat'
fn = 'maps.dat'

# Given a list of strings, rotate char grid 90 degrees
def rotate_map(cur_map):
    # Python trickery for rotating a list of strings
    return [''.join(row) for row in zip(*cur_map[::-1])]

# Check for a vertical reflection among lines
def check_ref1(cur_map):
    # Test each number as a mid-point
    for mid in range(0, len(cur_map)-1):
        no_match = False
        for offset in range(0, len(cur_map)-mid-1):
            idx1, idx2 = mid-offset, mid+offset+1

            # If hit top, then was good
            if idx1 < 0:
                return mid

            if cur_map[idx1] != cur_map[idx2]:
                no_match = True
                break

        if (not no_match):
            return mid

    return None

# Check for a vertical reflection among lines, requiring exactly one line to
# be "fixed" by changing one character. It just allows equality for exactly
# one line with exactly one character difference, and requires it to have
# happened to be considered the reflection we want.
def check_ref2(cur_map):
    # Test each number as a mid-point
    for mid in range(0, len(cur_map)-1):
        no_match = False
        had_fix = False
        for offset in range(0, len(cur_map)-mid-1):
            idx1, idx2 = mid-offset, mid+offset+1

            # If hit top, then stop
            if idx1 < 0:
                break

            if cur_map[idx1] != cur_map[idx2]:
                if had_fix:
                    no_match = True
                    break

                # Python trickery to generate list of character differences
                diffs = [(i, (c1, c2)) for i, (c1, c2) in enumerate(zip(cur_map[idx1], cur_map[idx2])) if c1 != c2]

                # Allow exactly one fix on one line
                if len(diffs) != 1:
                    no_match = True
                    break

                # Keep trying
                had_fix = True

        if not no_match and had_fix:
            return mid

    return None

# Open file and read each map one at a time
def get_next_map():
    cur_map = []
    for line in (line.strip() for line in open(fn, 'r')):
        if line == '':
            yield cur_map
            cur_map = []
        else:
            cur_map.append(line)
    if cur_map:
        yield cur_map

# Main processing. Read maps and calculate answer.
def main(part):
    # Figure out any row / column reflections and calculate summary answer
    check_ref = check_ref1 if part == 1 else check_ref2
    total = 0
    for cur_map in get_next_map():
        # First check row reflection
        row = check_ref(cur_map)
        if row != None:
            total += 100 * (row + 1)

        # Second check column reflection
        flipped_map = rotate_map(cur_map)
        col = check_ref(flipped_map)
        if col != None:
            total += (col + 1)

    return total

print(f"Total summary number is {main(1)}")
print(f"Total summary number is {main(2)}")
