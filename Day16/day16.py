#!/usr/bin/python
"""Advent of Code 2023, Day 16, Part 1

https://adventofcode.com/2023/day/16

Given a grid of mirrors and prisms, track the reflected rays and count how many
tiles are crossed by light rays. If a prism, then light splits in two paths.
For part 2, we need to scan coming in from different directions to see which is
optimal.

Uses a recursive algorithm, plus a cache to detect if a path is being retraced
in the same direction

See test.dat for sample data and sequence.dat for full data.

Author: Tim Behrendsen
"""

fn = 'test.dat'
fn = 'grid.dat'

movement = {
    '/':  { 'N': 'E', 'S': 'W', 'E': 'N', 'W': 'S' },
    '\\': { 'N': 'W', 'S': 'E', 'E': 'S', 'W': 'N' },
}

class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.num_rows, self.num_cols = len(grid), len(grid[0])
        self.reset_counts()

    def reset_counts(self):
        # Cache to see if we've seen a ray direction before
        self.cache = set()

        # Keep track as grid is traversed
        self.visited = set()

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
        while 0 <= row < self.num_rows and 0 <= col < self.num_cols:
            key = (row, col, d)
            if key in self.cache:
                return                      # Already seen this location + direction
            self.cache.add(key)

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

            self.visited.add((row, col))     # Mark visited
            dr, dc = {'N':(-1, 0), 'S':(1, 0), 'E':(0, 1), 'W':(0, -1)}[d]
            row, col = row+dr, col+dc

    # Do the ray processing, then count how many tiles were crossed.
    def count_energized(self, start_row, start_col, start_d):
        grid.reset_counts()
        self.scan_nodes(start_row, start_col, start_d)
        return len(self.visited)

def part1(grid):
    return grid.count_energized(0, 0, 'E')

def part2(grid):
    # Figure out optimal count, depending on which direction we come from
    max_count = 0
    for col in range(grid.num_cols):
        max_count = max(max_count, grid.count_energized(0, col, 'S'),
            grid.count_energized(grid.num_rows-1, col, 'N'))

    for row in range(grid.num_rows):
        max_count = max(max_count, grid.count_energized(row, 0, 'E'),
            grid.count_energized(row, grid.num_cols-1, 'W'))

    return max_count

grid = Grid([ line.rstrip() for line in open(fn, 'r') ])
print(f"Part 1: Total number energized tiles is {part1(grid)}")
print(f"Part 2: Maximum number energized tiles is {part2(grid)}")
