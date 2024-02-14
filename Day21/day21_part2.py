#!/usr/bin/python
"""Advent of Code 2023, Day 21, Part 2

https://adventofcode.com/2023/day/21

Given a garden plot map and a starting point, compute how many garden plots can be
reached by walking an exact number of steps. Backtracking is allowed, so the
starting point would be reachable by stepping back and forth.

Uses a modified Dijkstra's Algorithm to complete the distances. The tricky part
is that any node reached with an even number of steps, from any direction,
qualifies as reachable.

However, with Part 2, the garden is infinitely large by repeating the map pattern,
and we need to walk 26501365 steps.

There are a couple of key observations:
1) There is a repeating pattern of diamond shapes in the map.
2) 26501365 = 202300 * 131 + 65, and 131 is the size of the map.

It turns out that the step count follows a quadratic curve, and by calculating
the first few points, the formula can be fit to the data and then answer
computed.

The only last tricky part is that 26501365 is odd, so the progression
to be calculated needs to be odd numbers.

See test.dat for sample data and garden.dat for full data.

Author: Tim Behrendsen
"""

import re
import sys
import heapq
import numpy as np

fn = 'garden.dat'

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
        self.total_even = 0
        self.max_dist = 0

        # Map from node key to 
        self.node_map = { }

        # First find start row, col
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.garden_map[row][col] == 'S':
                    self.start_row = row
                    self.start_col = col
                    break

    #
    # Get character from the map, accounting that it can go in infinite directions
    #
    def get_map(self, row, col):
        return self.garden_map[row % self.num_rows][col % self.num_cols]

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

        # Initial potential directions are one step south and one step east.
        # Note we initialize to the cost for each direction.
        start_node = self.get_node(self.start_row, self.start_col)
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
            if self.get_map(cur_row-1, cur_col) != '#':
                move_list.append(self.get_node(cur_row-1, cur_col))
            if self.get_map(cur_row+1, cur_col) != '#':
                move_list.append(self.get_node(cur_row+1, cur_col))
            if self.get_map(cur_row, cur_col-1) != '#':
                move_list.append(self.get_node(cur_row, cur_col-1))
            if self.get_map(cur_row, cur_col+1) != '#':
                move_list.append(self.get_node(cur_row, cur_col+1))

            new_dist = cur_node.tent_dist + 1
            if new_dist > (max_steps+1):
                break

            if new_dist > self.max_dist:
                #print(f"new_dist = {new_dist}, total even = {self.total_even}")
                self.max_dist = new_dist

            is_even = new_dist % 2 == 0
            for new_node in move_list:
                if new_dist < new_node.tent_dist:
                    #new_node.prior_node = cur_node
                    # If first examination of node, add to priority queue
                    if new_node.tent_dist == sys.maxsize:
                        heapq.heappush(unv_set, new_node)

                    new_node.tent_dist = new_dist
                    if is_even and not new_node.is_even:
                        new_node.is_even = True
                        self.total_even += 1

            cur_node.visited = True

        # Find all nodes that had even distances
        num_plots = 0
        for key in self.node_map:
            node = self.node_map[key]
            if node.is_even:
                num_plots += 1

        return num_plots

#
# Main processing.
#
def main():
    # Read in the maps, each as an array of strings
    m = []
    with open(fn, 'r') as file:
        for line in file:
            line = line.rstrip('\n')
            m.append(line)

    # First calculate steps for 1, 3 and 5
    x_list = []
    y_list = []
    for mult in range(1, 6, 2):
        steps = 131 * mult + 65
        garden = Garden(m)
        total = garden.calc_paths(steps)
        x_list.append(mult)
        y_list.append(total)

    # Use numpy to calculate quadratic coefficients
    coeff = np.polyfit(x_list, y_list, 2)
    a, b, c = round(coeff[0]), round(coeff[1]), round(coeff[2])

    # Target: 26501365 = 202300 * 131 + 65
    # x = 202300
    x = 202300
    steps = a*x**2 + b*x + c

    return steps

total = main()
print(f"Count is {total}")
