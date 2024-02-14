#!/usr/bin/python
"""Advent of Code 2023, Day 16, Part 2

https://adventofcode.com/2023/day/16

Given a grid of mirrors and prisms, track the reflected rays and count how many
tiles are crossed by light rays. If a prism, then light splits in two paths.

Uses a recursive algorithm, plus a cache to detect if a path is being retraced
in the same direction. For Part 2, we need to scan coming in from different
directions to see which is optimal.

See test.dat for sample data and sequence.dat for full data.

Author: Tim Behrendsen
"""

import re
import sys

fn = 'test.dat'
fn = 'grid.dat'

movement = {
    '/': {
        'N': 'E',
        'S': 'W',
        'E': 'N',
        'W': 'S',
    },
    '\\': {
        'N': 'W',
        'S': 'E',
        'E': 'S',
        'W': 'N',
    },
}

class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.num_rows = len(grid)
        self.num_cols = len(grid[0])

        self.reset_counts()

    def reset_counts(self):
        # Cache to see if we've seen a ray direction before
        self.cache = set()

        # Keep track as grid is traversed
        self.node_marks = []
        for row in range(self.num_rows):
            self.node_marks.append([ False ] * self.num_cols)

    #
    # Recursively scan paths, splitting at prisms.
    #     / : Reflect
    #     \ : Reflect
    #     | : Split or pass
    #     - : Split or pass
    #
    # If a ray exits the grid, it just exits.
    #
    def scan_nodes(self, row, col, d):
        # First time through, we'll skip the cache check, because we're coming in
        # to the first node
        first = True

        while True:
            if not first:
                # Check cache to see if we've seen a ray going this direction before
                key = f"{row}-{col}-{d}"
                if key in self.cache:
                    return
                self.cache.add(key)

                self.node_marks[row][col] = True

                if d == 'N':
                    row -= 1
                elif d == 'S':
                    row += 1
                elif d == 'E':
                    col += 1
                elif d == 'W':
                    col -= 1

                if row < 0 or row >= self.num_rows or col < 0 or col >= self.num_cols:
                    return

            first = False

            c = self.grid[row][col]
            if c == '/':
                d = movement[c][d]
            elif c == '\\':
                d = movement[c][d]
            elif c == '|':
                if d == 'E' or d == 'W':
                    self.scan_nodes(row, col, 'N')
                    self.scan_nodes(row, col, 'S')
                    return
            elif c == '-':
                if d == 'N' or d == 'S':
                    self.scan_nodes(row, col, 'E')
                    self.scan_nodes(row, col, 'W')
                    return

    #
    # Do the ray processing, then count how many tiles were crossed.
    #
    def count_energized(self, start_row, start_col, start_d):
        self.scan_nodes(start_row, start_col, start_d)

        count = 0
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.node_marks[row][col]:
                    count += 1

        return count

#
# Main processing.
#
def main():
    # Read in all the maps, each as an array of strings
    g = []
    with open(fn, 'r') as file:
        for line in file:
            line = line.rstrip('\n')
            g.append(line)

    num_rows = len(g)
    num_cols = len(g[0])
    max_count = 0
    grid = Grid(g)

    # Figure out optimal count, depending on which direction we come from

    for col in range(num_cols):
        # Scan down from top
        grid.reset_counts()
        count = grid.count_energized(0, col, 'S')
        max_count = max(max_count, count)

        # Scan up from bottom
        grid.reset_counts()
        count = grid.count_energized(num_rows-1, col, 'N')
        max_count = max(max_count, count)

    for row in range(num_rows):
        # Scan in from left
        grid.reset_counts()
        count = grid.count_energized(row, 0, 'E')
        max_count = max(max_count, count)

        # Scan in from right
        grid.reset_counts()
        count = grid.count_energized(row, num_cols-1, 'W')
        max_count = max(max_count, count)

    return max_count

count = main()
print(f"Maximum number energized tiles is {count}")
