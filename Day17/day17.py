#!/usr/bin/python
"""Advent of Code 2023, Day 17

https://adventofcode.com/2023/day/17

Given a map of heat values, calculate the optimal path to minimize the heat.
However, the path must follow these rules:

1) Start at upper left, and can either go south or east.
2) First node is not counted in heat total
3) Can move in same direction only a maximum of 3 moves
4) End at lower right.

Uses Dijkstra's Algorithm with a four dimensional graph of row, column,
direction and number of steps in that direction.

See test.dat for sample data and map.dat for full data.

Author: Tim Behrendsen
"""

import sys, heapq

fn = 'test.dat'
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

        # Visited flag and tentative distance for Dijkstra
        self.visited = False
        self.tent_heat = sys.maxsize

    def __lt__(self, other):
        return self.tent_heat < other.tent_heat

class HeatMap:
    def __init__(self, m):
        self.heat_map = m
        self.num_rows = len(m)
        self.num_cols = len(m[0])

        # Map from node key to 
        self.node_map = { }

    #
    # Get node from node map, creating node if it doesn't exist
    # 
    def get_node(self, row, col, d, steps):
        key = (row, col, d, steps)
        node = self.node_map.get(key)
        if node == None:
            node = Node(row, col, d, steps)
            self.node_map[key] = node
        return node

    #
    # Compute optimal path using Dijkstra's Algorithm
    #
    def calc_min_heat(self, part):
        self.min_heat = 0
        self.node_map = { }
        start_row = 0
        start_col = 0

        if part == 1:
            min_moves, max_moves = 1, 3
        else:
            min_moves, max_moves = 4, 10

        # Initial potential directions are one step south and one step east.
        # Note we initialize to the cost for each direction.
        start_node1 = self.get_node(start_row+1, start_col, 'S', 1)
        start_node1.tent_heat = int(self.heat_map[start_row+1][start_col])

        start_node2 = self.get_node(start_row, start_col+1, 'E', 1)
        start_node2.tent_heat = int(self.heat_map[start_row][start_col+1])

        # Unvisited set, which will be a priority queue
        unv_set = [ start_node1, start_node2 ]

        while unv_set:
            cur_node = heapq.heappop(unv_set)

            # Figure out neighbor nodes and mark distances of neighbor nodes
            move_list = []
            for new_d in valid_dirs[cur_node.dir]:

                if part == 1:
                    new_steps = 1

                # Part 1: Only three moves in same direction
                # Part 2: Must be minimum four move in same direction, and
                #   must be maximum ten moves in same direction (below)
                if new_d == cur_node.dir:
                    new_steps = cur_node.steps+1
                    if new_steps > max_moves: ##
                        continue        # Skip same direction, must turn

                # Part 2: No turning unless we've had four in same direction
                if part == 2 and new_d != cur_node.dir:
                    if cur_node.steps < min_moves:
                        continue

                    # Turning, so this will be step 1
                    new_steps = 1

                # Process new move
                dr, dc = {'N':(-1, 0), 'S':(1, 0), 'W':(0, -1), 'E':(0, 1)}[new_d]
                new_row, new_col = cur_node.row+dr, cur_node.col+dc
                if not (0 <= new_row < self.num_rows and 0 <= new_col < self.num_cols):
                    continue

                new_heat_total = cur_node.tent_heat + int(self.heat_map[new_row][new_col])
                new_node = self.get_node(new_row, new_col, new_d, new_steps)
                if new_heat_total < new_node.tent_heat:
                    # If first examination of node, add to priority queue
                    if new_node.tent_heat == sys.maxsize:
                        heapq.heappush(unv_set, new_node)

                    new_node.tent_heat = new_heat_total

                cur_node.visited = True

        last_row = self.num_rows-1
        last_col = self.num_cols-1
        best_node = None

        # Scan for best node, but in part 2, number of final steps must have been
        # four or more in the same direction.
        for key in self.node_map:
            node = self.node_map[key]
            if node.row == last_row and node.col == last_col and node.steps >= min_moves:
                if best_node == None or best_node.tent_heat > node.tent_heat:
                    best_node = node

        return best_node.tent_heat

# Read in all the maps, each as an array of strings
heat_map = HeatMap([line.strip() for line in open(fn, 'r')])
print(f"Part 1: Best total heat is {heat_map.calc_min_heat(part=1)}")
print(f"Part 2: Best total heat is {heat_map.calc_min_heat(part=2)}")
