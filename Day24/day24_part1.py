#!/usr/bin/python
"""Advent of Code 2023, Day 24, Part 1

https://adventofcode.com/2023/day/24

Given coordinates and velocities of "hailstones", consider just the X, Y
coordinates and calculate how many hailstones' paths will intersect within
a specific test area.

See test.dat for sample data and paths.dat for full data.

Author: Tim Behrendsen
"""

import re
import sys

fn = 'test.dat'
min_coord = 7
max_coord = 27

fn = 'paths.dat'
min_coord = 200000000000000
max_coord = 400000000000000

class Hailstone:
    def __init__(self, x, y, z, dx, dy, dz):
        self.x, self.y, self.z = int(x), int(y), int(z)
        self.dx, self.dy, self.dz = int(dx), int(dy), int(dz)

    def __repr__(self):
        return f"[{self.x}, {self.y}, {self.z} / {self.dx}, {self.dy}, {self.dz}]"

    # Return intersection point of pair of stones. Returns ('P','P') if lines
    # don't intersect (Parallel lines).
    def intersect(self, other):
        # Unpack points
        (x1, y1), (x2, y2) = (self.x, self.y), (self.x + self.dx, self.y + self.dy)
        (a1, b1), (a2, b2) = (other.x, other.y), (other.x + other.dx, other.y + other.dy)

        # Calculate the slopes of the lines, handling vertical lines
        if x2 - x1 == 0:  # Line 1 is vertical
            m1 = None
        else:
            m1 = (y2 - y1) / (x2 - x1)

        if a2 - a1 == 0:  # Line 2 is vertical
            m2 = None
        else:
            m2 = (b2 - b1) / (a2 - a1)

        # Check if lines are parallel (including both vertical)
        if m1 == m2:
            return ('P', 'P')

        # Calculate intercepts, handling vertical lines
        if m1 is not None:
            b1_line = y1 - m1 * x1
        if m2 is not None:
            b2_line = b1 - m2 * a1

        # If one of the lines is vertical, calculate intersection directly
        if m1 is None:
            x = x1
            y = m2 * x + b2_line
            return (x, y)
        if m2 is None:
            x = a1
            y = m1 * x + b1_line
            return (x, y)

        # Calculate intersection point for non-vertical lines
        x = (b2_line - b1_line) / (m1 - m2)
        y = m1 * x + b1_line
        return (x, y)

#
# Main processing.
#
def main():
    # Read in all the maps, each as an array of strings
    stone_list = []
    with open(fn, 'r') as file:
        for line in file:
            line = line.rstrip('\n')
            matches = re.findall(r'(-?\d+)', line)
            stone = Hailstone(*matches)
            stone_list.append(stone)

    # For each pair of hailstones, calculate intersection point and decide
    # if they'll intersect within our test area forward in time.
    count = 0
    for idx1 in range(len(stone_list)-1):
        stone1 = stone_list[idx1]
        for idx2 in range(idx1+1, len(stone_list)):
            stone2 = stone_list[idx2]
            (x, y) = stone1.intersect(stone2)

            # If parallel, no intersection
            if x == 'P':
                continue

            # Check if intersecting back in time
            back_flag = False
            if stone1.dx != 0:
                if stone1.dx < 0 and x > stone1.x:
                    back_flag = True
                elif stone1.dx > 0 and x < stone1.x:
                    back_flag = True
            else:
                if stone1.yx < 0 and y > stone1.y:
                    back_flag = True
                elif stone1.dy > 0 and y < stone1.y:
                    back_flag = True

            if stone2.dx != 0:
                if stone2.dx < 0 and x > stone2.x:
                    back_flag = True
                elif stone2.dx > 0 and x < stone2.x:
                    back_flag = True
            else:
                if stone2.yx < 0 and y > stone2.y:
                    back_flag = True
                elif stone2.dy > 0 and y < stone2.y:
                    back_flag = True

            if back_flag:
                continue

            if (min_coord <= x <= max_coord) and (min_coord <= y <= max_coord):
                count += 1

    return count

total = main()
print(f"Count is {total}")
