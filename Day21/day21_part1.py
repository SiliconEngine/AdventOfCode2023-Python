#!/usr/bin/python
"""Advent of Code 2023, Day 21, Part 1

https://adventofcode.com/2023/day/21

Given a garden plot map and a starting point, compute how many garden plots can be
reached by walking an exact number of steps. Backtracking is allowed, so the
starting point would be reachable by stepping back and forth.

Uses a modified Dijkstra's Algorithm to complete the distances. The tricky part
is that any node reached with an even number of steps, from any direction,
qualifies as reachable.

See test.dat for sample data and garden.dat for full data.

Author: Tim Behrendsen
"""

import re
import sys
import heapq

#fn = 'test.dat'
#MAX_STEPS = 6

fn = 'garden.dat'
MAX_STEPS = 64

# Display map after completion
SHOW_MAP = True

#
# Class to hold node information for path search
#
class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col

        # Visited flag and tentative distance for Dijkstra
        self.visited = False
        self.tent_dist = sys.maxsize

        # Keep track if we find an even distance to this node
        self.is_even = False

    def __repr__(self):
        dist = "inf" if self.tent_dist == sys.maxsize else self.tent_dist
        return f"[{self.row}, {self.col}: dist={dist}]"

    def __lt__(self, other):
        return self.tent_dist < other.tent_dist

    def get_key(self):
        return self.make_key(self.row, self.col)

    @staticmethod
    def make_key(row, col):
        return f"{row}-{col}"

#
# Class for garden map
#
class Garden:
    def __init__(self, m):
        self.garden_map = m
        self.num_rows = len(m)
        self.num_cols = len(m[0])

        # Map from node key to 
        self.node_map = { }

    #
    # Get node from node map, creating node if it doesn't exist
    # 
    def get_node(self, row, col):
        key = Node.make_key(row, col)
        node = self.node_map.get(key)
        if node != None:
            return node

        node = Node(row, col)
        self.node_map[key] = node
        return node

    #
    # Compute optimal path using Dijkstra's Algorithm
    #
    def calc_paths(self, max_steps):

        # First find start row, col
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.garden_map[row][col] == 'S':
                    start_row = row
                    start_col = col
                    break

        # Initial potential directions are one step south and one step east.
        # Note we initialize to the cost for each direction.
        start_node = self.get_node(start_row, start_col)
        start_node.tent_dist = 0
        start_node.is_even = True

        # Unvisited set, which will be a priority queue
        unv_set = [ start_node ]

        while unv_set:
            cur_node = heapq.heappop(unv_set)
            cur_row = cur_node.row
            cur_col = cur_node.col

            # Figure out neighbor nodes and mark distances of neighbor nodes
            move_list = []
            if cur_row > 0 and self.garden_map[cur_row-1][cur_col] != '#':
                move_list.append(self.get_node(cur_row-1, cur_col))
            if cur_row < (self.num_rows-1) and self.garden_map[cur_row+1][cur_col] != '#':
                move_list.append(self.get_node(cur_row+1, cur_col))
            if cur_col > 0 and self.garden_map[cur_row][cur_col-1] != '#':
                move_list.append(self.get_node(cur_row, cur_col-1))
            if cur_col < (self.num_cols-1) and self.garden_map[cur_row][cur_col+1] != '#':
                move_list.append(self.get_node(cur_row, cur_col+1))

            new_dist = cur_node.tent_dist + 1
            is_even = new_dist % 2 == 0
            for new_node in move_list:
                if new_dist < new_node.tent_dist:
                    #new_node.prior_node = cur_node
                    # If first examination of node, add to priority queue
                    if new_node.tent_dist == sys.maxsize:
                        heapq.heappush(unv_set, new_node)

                    new_node.tent_dist = new_dist
                    if is_even:
                        new_node.is_even = True

            cur_node.visited = True

        # Find all nodes that had even distances
        num_plots = 0
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.garden_map[row][col] != '#':
                    node = self.get_node(row, col)
                    if node.is_even and node.tent_dist <= max_steps:
                        num_plots += 1


        if (SHOW_MAP):
            # Find all nodes that had even distances
            for row in range(self.num_rows):
                for col in range(self.num_cols):
                    if self.garden_map[row][col] == '#':
                        print('#', end='')
                    else:
                        node = self.get_node(row, col)
                        if node.is_even and node.tent_dist <= max_steps:
                            print('O', end='')
                        else:
                            print('.', end='')

                print()

        return num_plots

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

    garden = Garden(m)
    total = garden.calc_paths(MAX_STEPS)

    return total

total = main()
print(f"Count is {total}")
