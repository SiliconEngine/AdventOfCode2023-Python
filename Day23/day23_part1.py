#!/usr/bin/python
"""Advent of Code 2023, Day 23, Part 1

https://adventofcode.com/2023/day/23

Given a map of trails, compute the longest path, accounting for arrows that
restrict movements in certain directions, and you can't backtrack onto a tile
already visited. Uses a depth-first-search to compute the longest path.

See test.dat for sample data and trails.dat for full data.

Author: Tim Behrendsen
"""

import re
import sys

fn = 'test.dat'
fn = 'trails.dat'

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

        # Map from node key to node
        self.node_map = { }

    #
    # Compute longest path using depth-first-search
    #
    def calc_paths(self):
        start_row = 0
        start_col = 1

        # Initialize start node
        chk_set = set()
        start_node = Node(start_row, start_col, 0, chk_set)
        start_node.tent_dist = 0

        # Processing stack for DFS
        q = [ start_node ]

        end_list = []
        while q:
            cur_node = q.pop()

            cur_row = cur_node.row
            cur_col = cur_node.col
            key = f"{cur_row}-{cur_col}"
            cur_node.chk_set.add(key)

            if cur_row == self.num_rows-1:
                #end_node = cur_node
                dist = cur_node.cur_dist
                print(f"END: dist = {dist}")
                end_list.append(dist)
                continue

            # Figure out neighbor nodes and mark distances of neighbor nodes
            move_list = []
            new_dist = cur_node.cur_dist + 1

            def check_valid(new_row, new_col, bad_c, chk_set):
                if self.trail_map[new_row][new_col] in ('#', bad_c):
                    return False
                key = f"{new_row}-{new_col}"
                return key not in chk_set

            # Up
            if cur_row > 0 and check_valid(cur_row-1, cur_col, 'v', cur_node.chk_set):
            #if cur_row > 0 and self.trail_map[cur_row-1][cur_col] not in ('#', 'v'):
                move_list.append(Node(cur_row-1, cur_col, new_dist))

            # Down
            if cur_row < (self.num_rows-1) and check_valid(cur_row+1, cur_col, '^', cur_node.chk_set):
                move_list.append(Node(cur_row+1, cur_col, new_dist))

            # Left
            if cur_col > 0 and check_valid(cur_row, cur_col-1, '>', cur_node.chk_set):
                move_list.append(Node(cur_row, cur_col-1, new_dist))

            # Right
            if cur_col < (self.num_cols-1) and check_valid(cur_row, cur_col+1, '<', cur_node.chk_set):
                move_list.append(Node(cur_row, cur_col+1, new_dist))

            if len(move_list) == 1:
                # If only one new direction, can use same check set

                move_list[0].chk_set = cur_node.chk_set
                q.append(move_list[0])
            else:
                # Multiple new directions, need to separate check sets
                for node in move_list:
                    node.chk_set = cur_node.chk_set.copy()
                    q.append(node)

        n = 0
        for n2 in end_list:
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
