#!/usr/bin/python
"""Advent of Code 2023, Day 17, Part 2

https://adventofcode.com/2023/day/17

Given a map of heat values, calculate the optimal path to minimize the heat.
However, the path must follow these rules:

1) Start at upper left, and can either go south or east.
2) First node is not counted in heat total
3) Can move in same direction only a maximum of 10 moves.
4) Must move same direction a minimumum of 4 moves.
5) End at lower right.
6) Must end with at least the minimum 4 in same direction.

Uses Dijkstra's Algorithm with a four dimensional graph of row, column,
direction and number of steps in that direction.

See test.dat + test2.dat for sample data and map.dat for full data.

Author: Tim Behrendsen
"""

import re
import sys
import heapq

fn = 'test.dat'
fn = 'test2.dat'
fn = 'map.dat'

valid_dirs = {
    'S': [ 'S', 'E', 'W' ],
    'N': [ 'N', 'E', 'W' ],
    'E': [ 'E', 'N', 'S' ],
    'W': [ 'W', 'N', 'S' ],
}

#
# Class to heat value on map, along with direction and steps
#
class Node:
    def __init__(self, row, col, d, steps):
        self.row = row
        self.col = col
        self.dir = d
        self.steps = steps

        # So we can reconstruct path for debugging
        self.prior_node = None

        # Visited flag and tentative distance for Dijkstra
        self.visited = False
        self.tent_heat = sys.maxsize

    def __repr__(self):
        dist = "inf" if self.tent_heat == sys.maxsize else self.tent_heat
        return f"[{self.row}, {self.col}: {self.dir} / {self.steps} heat={dist}]"

    def __lt__(self, other):
        return self.tent_heat < other.tent_heat

    def get_key(self):
        return self.make_key(self.row, self.col, self.dir, self.steps)

    @staticmethod
    def make_key(row, col, d, steps):
        return f"{row}-{col}-{d}{steps}"


class HeatMap:
    def __init__(self, m):
        self.heat_map = m
        self.num_rows = len(m)
        self.num_cols = len(m[0])
        self.min_heat = 0

        # Map from node key to 
        self.node_map = { }

    #
    # Get node from node map, creating node if it doesn't exist
    # 
    def get_node(self, row, col, d, steps):
        key = Node.make_key(row, col, d, steps)
        node = self.node_map.get(key)
        if node != None:
            return node

        node = Node(row, col, d, steps)
        self.node_map[key] = node
        return node

    #
    # Display optimal path back to start from node
    #
    def dsp_path(self, node):
        print(f"PATH:")
        total = 0
        while node != None:
            total += int(self.heat_map[node.row][node.col])
            print(f"Node: {node}, total = {total}")
            node = node.prior_node

    #
    # Compute optimal path using Dijkstra's Algorithm
    #
    def calc_min_heat(self):
        start_row = 0
        start_col = 0

        # Initial potential directions are one step south and one step east.
        # Note we initialize to the cost for each direction.
        start_node1 = self.get_node(start_row+1, start_col, 'S', 1)
        start_node1.tent_heat = int(self.heat_map[start_row+1][start_col])

        start_node2 = self.get_node(start_row, start_col+1, 'E', 1)
        start_node2.tent_heat = int(self.heat_map[start_row][start_col+1])

        # Unvisited set, which will be a priority queue
        unv_set = [ start_node1, start_node2 ]

        num_visits = 0

        while unv_set:
            cur_node = heapq.heappop(unv_set)

            # Figure out neighbor nodes and mark distances of neighbor nodes
            move_list = []
            for new_d in valid_dirs[cur_node.dir]:

                # Must be minimum four move in same direction.
                # must be maximum ten moves in same direction
                if new_d == cur_node.dir:
                    new_steps = cur_node.steps+1
                    if new_steps > 10:
                        continue        # Skip same direction, must turn

                # No turning unless we've had four in same direction
                if new_d != cur_node.dir:
                    if cur_node.steps < 4:
                        continue

                    # Turning, so this will be step 1
                    new_steps = 1

                # Process new move
                new_row = cur_node.row
                new_col = cur_node.col
                if new_d == 'N':
                    if new_row == 0:
                        continue
                    new_row -= 1
                if new_d == 'S':
                    if new_row == (self.num_rows-1):
                        continue
                    new_row += 1
                if new_d == 'W':
                    if new_col == 0:
                        continue
                    new_col -= 1
                if new_d == 'E':
                    if new_col == (self.num_cols-1):
                        continue
                    new_col += 1

                new_heat_total = cur_node.tent_heat + int(self.heat_map[new_row][new_col])
                new_node = self.get_node(new_row, new_col, new_d, new_steps)
                if new_heat_total < new_node.tent_heat:
                    new_node.prior_node = cur_node
                    # If first examination of node, add to priority queue
                    if new_node.tent_heat == sys.maxsize:
                        heapq.heappush(unv_set, new_node)

                    new_node.tent_heat = new_heat_total

                cur_node.visited = True
                num_visits += 1

        last_row = self.num_rows-1
        last_col = self.num_cols-1
        best_node = None

        # Scan for best node, but number of final steps must have been
        # four or more in the same direction
        for key in self.node_map:
            node = self.node_map[key]
            if node.row == last_row and node.col == last_col and node.steps >= 4:
                if best_node == None or best_node.tent_heat > node.tent_heat:
                    best_node = node

        #self.dsp_path(best_node)
        return best_node.tent_heat

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


    heat_map = HeatMap(m)
    heat = heat_map.calc_min_heat()

    return heat

heat = main()
print(f"Best total heat is {heat}")
