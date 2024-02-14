#!/usr/bin/python
"""Advent of Code 2023, Day 11, Part 2

https://adventofcode.com/2023/day/11

Given a map of galaxies, figure out the total of the taxi distance between each
pair of them. However, if there are rows without galaxies, each of those rows count
as one million, and columns without galaxies also count as one million.

See test.dat for sample data and image.dat for full data.

Author: Tim Behrendsen
"""

import re
import sys

fn = 'test.dat'
fn = 'image.dat'

#
# Class to hold position on image map
#
class Node:
    def __init__(self, row, col, type):
        self.row = row
        self.col = col

    def __repr__(self):
        return f"[{self.row}, {self.col}]"

#
# Main processing. Return total of distances between pairs of galaxies
#
def main():
    # Read the map of images
    galaxies = []
    row_set = set()
    col_set = set()
    num_rows = 0
    num_cols = 0
    with open(fn, 'r') as file:
        row = 0
        for line in file:
            line = line.rstrip('\n')
            col = 0
            for c in line:
                if c == '#':
                    node = Node(row, col, c)
                    galaxies.append(node)
                    row_set.add(row)
                    col_set.add(col)

                col += 1

            num_cols = max(num_cols, col)
            row += 1

    num_rows = row

    # Figure out what rows and columns are missing galaxies
    missing_cols = []
    for col in range(num_cols):
        if col not in col_set:
            missing_cols.append(col)

    missing_rows = []
    for row in range(num_rows):
        if row not in row_set:
            missing_rows.append(row)

    # Replace empty rows/columns with this many rows/columns
    adj_factor = 1_000_000

    # Figure out coordinate adjustments based on increasing the size of
    # rows and columns without galaxies
    col_adj = []
    for idx in range(num_cols):
        col_adj.append(0)
    for col in missing_cols:
        for idx in range(col+1, num_cols):
            col_adj[idx] += (adj_factor-1)

    row_adj = []
    for idx in range(num_rows):
        row_adj.append(0)
    for row in missing_rows:
        for idx in range(row+1, num_rows):
            row_adj[idx] += (adj_factor-1)

    # Adjust the coordinates of the galaxies
    for node in galaxies:
        node.row += row_adj[node.row]
        node.col += col_adj[node.col]

    # Calculate taxi distance between each pair of galaxies
    total = 0
    for idx1 in range(len(galaxies)):
        node1 = galaxies[idx1]
        start_row = node1.row
        start_col = node1.col
        for idx2 in range(idx1+1, len(galaxies)):
            node2 = galaxies[idx2]
            end_row = node2.row
            end_col = node2.col
            dist = abs(end_row - start_row) + abs(end_col - start_col)
            total += dist

    return total

    exit(0)

total = main()
print(f"Total distance is {total}")
