#!/usr/bin/python

"""Advent of Code 2023, Day 23, Part 2

https://adventofcode.com/2023/day/23

Given a map of trails, compute the longest path, ignoring the arrows and allowing
free travel, but not backtracking onto an already-visited path.

This greatly increased the number of combinations, but longest-path algorithms
still require brute force. This eventually finished, but could be sped up with
a better data structure that compresses the map into just intersecting nodes,
rather than traversing the paths every time.

See test.dat for sample data and trails.dat for full data.

Author: Tim Behrendsen
"""

import re
import sys
import inspect

fn = 'test.dat'
fn = 'trails.dat'

RED = "\x1b[31m"
NORMAL = "\x1b[0m"

#
# Class to hold node information for path search
#
class Node:
    def __init__(self, row, col, cur_dist, chk_set = None):
        self.row = row
        self.col = col
        self.cur_dist = cur_dist
        self.chk_set = chk_set

        # So we can reconstruct path for debugging
        self.prior_node = None

        # Visited flag
        self.visited = False

    def __repr__(self):
        return f"[{self.row}, {self.col}: dist={self.cur_dist}]"

#
# Class for trail map
#
class Trails:
    def __init__(self, m):
        self.trail_map = m
        self.num_rows = len(m)
        self.num_cols = len(m[0])

        self.end_list = []
        self.max_dist = 0

    #
    # Display traveled path back from node
    #
    def dump_path(self, node):
        # Display the map
        chk_set = node.chk_set
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                c = self.trail_map[row][col]
                if c == '#':
                    print('#', end='')
                else:
                    key = f"{row}-{col}"
                    if key in chk_set:
                        print(RED + c + NORMAL, end='')
                    else:
                        print(c, end='')

            print()

    #
    # Recursive travel from current node
    #
    def recurse_paths(self, cur_node):
        while True:
            cur_row = cur_node.row
            cur_col = cur_node.col
            key = f"{cur_row}-{cur_col}"
            cur_node.chk_set.add(key)

            if cur_row == self.num_rows-1:
                dist = cur_node.cur_dist
                self.max_dist = max(self.max_dist, dist)
                print(f"END: dist = {dist}, max = {self.max_dist}, stack depth = {len(inspect.stack())}")
                self.end_list.append(dist)
                return dist

            # Figure out neighbor nodes and mark distances of neighbor nodes
            move_list = []
            new_dist = cur_node.cur_dist + 1

            def check_valid(new_row, new_col, chk_set):
                if self.trail_map[new_row][new_col] == '#':
                    return False
                key = f"{new_row}-{new_col}"
                return key not in chk_set

            # Up
            if cur_row > 0 and check_valid(cur_row-1, cur_col,  cur_node.chk_set):
                move_list.append((cur_row-1, cur_col, 'N'))

            # Down
            if cur_row < (self.num_rows-1) and check_valid(cur_row+1, cur_col,  cur_node.chk_set):
                move_list.append((cur_row+1, cur_col, 'S'))

            # Left
            if cur_col > 0 and check_valid(cur_row, cur_col-1,  cur_node.chk_set):
                move_list.append((cur_row, cur_col-1, 'W'))

            # Right
            if cur_col < (self.num_cols-1) and check_valid(cur_row, cur_col+1,  cur_node.chk_set):
                move_list.append((cur_row, cur_col+1, 'E'))

            if len(move_list) == 0:
                # No further paths from here (wrapped on ourself)
                return -1

            if len(move_list) == 1:
                # If only one new direction, can use same check set

                entry = move_list[0]
                cur_node.row = entry[0]
                cur_node.col = entry[1]
                cur_node.cur_dist = new_dist
                continue

            else:
                # Multiple new directions, need separate check sets and recursive call
                max_dist = 0
                for entry in move_list:
                    node = Node(entry[0], entry[1], new_dist)
                    node.chk_set = cur_node.chk_set.copy()
                    dist = self.recurse_paths(node)
                    if dist > 0:
                        max_dist = max(max_dist, dist)

                return max_dist

            print("BAD")
            break

        print("BAD")
        exit(0)

    #
    # Compute longest path using recursive depth-first-search
    #
    def calc_paths(self):
        self.max_dist = 0

        start_row = 0
        start_col = 1

        # Initialize start node
        chk_set = set()
        start_node = Node(start_row, start_col, 0, chk_set)

        total = self.recurse_paths(start_node)

        n = 0
        for n2 in self.end_list:
            n = max(n, n2)
        return n

#
# Main processing.
#
def main():
    # Read in all the maps, each as an array of strings
    m = []
    with open(fn, 'r') as file:
        for line in file:
            line = line.rstrip('\n')
            m.append(line)

    trails = Trails(m)
    total = trails.calc_paths()

    return total

total = main()
print(f"Count is {total}")
