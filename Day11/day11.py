#!/usr/bin/python
"""Advent of Code 2023, Day 11

https://adventofcode.com/2023/day/11

Given a map of galaxies, figure out the total of the taxi distance between each
pair of them. However, if there are rows without galaxies, each of those rows count
as two, and columns without galaxies also count as two. In part 2, each of those
rows count as one million, and columns without galaxies also count as one million.

See test.dat for sample data and image.dat for full data.

Author: Tim Behrendsen
"""

fn = 'test.dat'
fn = 'image.dat'

from types import SimpleNamespace as Galaxy

# Main processing. Return total of distances between pairs of galaxies
def calc(adj_factor):
    # Read the map of galaxies
    galaxies = []
    for row, line in enumerate(line.rstrip() for line in open(fn, 'r')):
        for col, c in enumerate(line):
            if c == '#':
                galaxies.append(Galaxy(row=row, col=col))

    row_set = set(g.row for g in galaxies)
    col_set = set(g.col for g in galaxies)
    num_cols, num_rows = max(col_set)+1, max(row_set)+1

    # Figure out what rows and columns are missing galaxies
    missing_cols = [ col for col in range(num_cols) if col not in col_set ]
    missing_rows = [ row for row in range(num_rows) if row not in row_set ]

    # Figure out coordinate adjustments based on doubling the rows and columns
    # without galaxies
    col_adj = [0] * num_cols
    for col in missing_cols:
        for idx in range(col+1, num_cols):
            col_adj[idx] += adj_factor-1

    row_adj = [0] * num_rows
    for row in missing_rows:
        for idx in range(row+1, num_rows):
            row_adj[idx] += adj_factor-1

    # Adjust the coordinates of the galaxies
    for node in galaxies:
        node.row += row_adj[node.row]
        node.col += col_adj[node.col]

    # Calculate taxi distance between each pair of galaxies and total
    total = 0
    for idx1 in range(len(galaxies)):
        node1 = galaxies[idx1]
        start_row, start_col = node1.row, node1.col
        for idx2 in range(idx1+1, len(galaxies)):
            node2 = galaxies[idx2]
            end_row, end_col = node2.row, node2.col
            total += abs(end_row - start_row) + abs(end_col - start_col)

    return total

# Part 1 adjusts by 2
print(f"Total distance is {calc(2)}")

# Part 2 adjusts by 1M
print(f"Total distance is {calc(1_000_000)}")
