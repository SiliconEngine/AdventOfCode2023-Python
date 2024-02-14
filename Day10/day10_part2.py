#!/usr/bin/python
"""Advent of Code 2023, Day 10, Part 2

https://adventofcode.com/2023/day/10

Given a series of pipes on a map and starting position, figure out what pipes
form a loop. Given the loop, then figure out how many nodes are fully enclosed
by the loop.

This implementation uses Dijkstra's Algorithm to figure the loop (from Part 1). Then
it uses the Even-Odd Rule to determine when each node is within the loop.

See part2_test1.dat and part2_test2.dat for sample data and pipes.dat for full data.

Author: Tim Behrendsen
"""

import re
import sys
import heapq

fn = 'part2_test1.dat'
fn = 'part2_test2.dat'
fn = 'pipes.dat'

class Node:
    def __init__(self, row, col, type):
        self.row = row
        self.col = col
        self.type = type

        # Visited flag and tentative distance for Dijkstra
        self.visited = False
        self.tent_dist = 0

        # Routes to other nodes
        self.routes = []

    def __repr__(self):
        dist = "inf" if self.tent_dist == sys.maxsize else self.tent_dist
        return f"[{self.row}, {self.col}: {self.type}, dist={dist}]"

    def __lt__(self, other):
        return self.tent_dist < other.tent_dist


class PipeMap:
    def __init__(self, pipe_map):
        self.pipe_map = pipe_map
        self.start_row = 0
        self.start_col = 0

    def dump_map(self):
        for pipe_row in self.pipe_map:
            for node in pipe_row:
                print(node, end='')
            print("")

    def dump_mode(self):
        for pipe_row in self.pipe_map:
            for node in pipe_row:
                print(node.mode, end='')
            print("")

    def dump_dist(self):
        for pipe_row in self.pipe_map:
            for node in pipe_row:
                if node.tent_dist == sys.maxsize:
                    dist = 'I'
                elif node.tent_dist < 10:
                    dist = node.tent_dist
                elif node.tent_dist > 10 and node.tent_dist < 36:
                    dist = chr(ord('A') + node.tent_dist - 10)
                else:
                    dist = '#'
                print(dist, end='')
            print("")

    # Build routes based on character values at each node
    #     | is a vertical pipe connecting north and south.
    #     - is a horizontal pipe connecting east and west.
    #     L is a 90-degree bend connecting north and east.
    #     J is a 90-degree bend connecting north and west.
    #     7 is a 90-degree bend connecting south and west.
    #     F is a 90-degree bend connecting south and east.
    #     . is ground; there is no pipe in this tile.
    #     S is starting position
    def build_routes(self, start_dir):
        max_row = len(self.pipe_map)-1
        max_col = len(self.pipe_map[0])-1

        for pipe_row in self.pipe_map:
            for node in pipe_row:
                row = node.row
                col = node.col
                type = node.type
                node.routes = []
                if type == '|':
                    if row > 0:
                        node.routes.append(self.pipe_map[row-1][col])
                    if row < max_row:
                        node.routes.append(self.pipe_map[row+1][col])

                elif type == '-':
                    if col > 0:
                        node.routes.append(self.pipe_map[row][col-1])
                    if col < max_col:
                        node.routes.append(self.pipe_map[row][col+1])

                elif type == 'L':
                    if row > 0:
                        node.routes.append(self.pipe_map[row-1][col])
                    if col < max_col:
                        node.routes.append(self.pipe_map[row][col+1])

                elif type == 'J':
                    if row > 0:
                        node.routes.append(self.pipe_map[row-1][col])
                    if col > 0:
                        node.routes.append(self.pipe_map[row][col-1])

                elif type == '7':
                    if row < max_row:
                        node.routes.append(self.pipe_map[row+1][col])
                    if col > 0:
                        node.routes.append(self.pipe_map[row][col-1])

                elif type == 'F':
                    if row < max_row:
                        node.routes.append(self.pipe_map[row+1][col])
                    if col < max_col:
                        node.routes.append(self.pipe_map[row][col+1])

                elif type == '.':
                    pass

                elif type == 'S':
                    self.start_row = row
                    self.start_col = col

                    # Starting position potentially can go four routes
                    if start_dir == 'N' and row > 0:
                        if self.pipe_map[row-1][col].type != '.':
                            node.routes.append(self.pipe_map[row-1][col])
                    if start_dir == 'S' and row < max_row:
                        if self.pipe_map[row+1][col].type != '.':
                            node.routes.append(self.pipe_map[row+1][col])
                    if start_dir == 'W' and col > 0:
                        if self.pipe_map[row][col-1].type != '.':
                            node.routes.append(self.pipe_map[row][col-1])
                    if start_dir == 'E' and col < max_col:
                        if self.pipe_map[row][col+1].type != '.':
                            node.routes.append(self.pipe_map[row][col+1])

    def search_routes(self):
        cur_row = self.start_row
        cur_col = self.start_col

        # Initialize tentative distances for the nodes
        for pipe_row in self.pipe_map:
            for node in pipe_row:
                node.visited = False
                node.tent_dist = sys.maxsize

        start_node = self.pipe_map[self.start_row][self.start_col]
        start_node.tent_dist = 0

        # Unvisited set, which will be a priority queue
        unv_set = [ start_node ]

        heapq.heapify(unv_set)

        while unv_set:
            cur_node = heapq.heappop(unv_set)

            # Mark distances of neighbor nodes
            new_dist = cur_node.tent_dist + 1
            for node in cur_node.routes:
                if not node.visited:
                    if new_dist < node.tent_dist:
                        # If first examination of node, add to priority queue
                        if node.tent_dist == sys.maxsize:
                            heapq.heappush(unv_set, node)

                        node.tent_dist = new_dist

            cur_node.visited = True

        ##self.dump_dist()

        # Find greatest distance
        dist = 0
        for pipe_row in self.pipe_map:
            for node in pipe_row:
                if (node.tent_dist != sys.maxsize):
                    dist = max(dist, node.tent_dist)

        return dist


def main():
    # Read the map of pipes
    build_map = []
    total = 0
    with open(fn, 'r') as file:
        row = 0
        for line in file:
            pipe_row = []
            line = line.rstrip('\n')
            col = 0
            for c in line:
                node = Node(row, col, c)
                pipe_row.append(node)
                col += 1

            build_map.append(pipe_row)
            row += 1

    pipe_map = PipeMap(build_map)

    # Try each direction. The loop should have two of the same direction and the distance will
    # be all the way around. So our furthest distance is (dist + 1)/2.
    dist_list = []
    for start_dir in ['N', 'S', 'E', 'W']:
        pipe_map.build_routes(start_dir)
        dist = pipe_map.search_routes()
        dist_list.append((start_dir, dist))

    dist_list.sort(key=lambda e: e[1], reverse=True)
    if (dist_list[0][1] != dist_list[1][1]):
        raise Exception(f"Expected first two to be equal, instead was: {dist_list}")

    real_dist = (dist_list[0][1]+1)/2
    both_dirs = dist_list[0][0] + dist_list[1][0]
    if both_dirs == 'SE' or both_dirs == 'ES':
        start_pipe = 'F'
    elif both_dirs == 'NE' or both_dirs == 'EN':
        start_pipe = 'L'
    elif both_dirs == 'SW' or both_dirs == 'WS':
        start_pipe = '7'
    elif both_dirs == 'NW' or both_dirs == 'WN':
        start_pipe = 'J'

    pipe_map.build_routes(start_dir)
    dist = pipe_map.search_routes()

    #pipe_map.dump_dist()

    pipe_map.pipe_map[pipe_map.start_row][pipe_map.start_col].type = start_pipe

    # Do Even/Odd rule algorithm by flipping flag depending on whether we cross over a
    # pipe connection. Flip rules:
    #     1: | (flip)
    #     2: - (no flip)
    #     2: F paired with 7 (no flip)
    #     3: F paired with J (flip)
    #     4: L paired with 7 (flip)
    #     5: L paired with J (no flip)
    cur_type = ''
    inside_count = 0
    outside_count = 0
    pipe_count = 0
    for pipe_row in pipe_map.pipe_map:
        mode = False
        for node in pipe_row:
            if node.tent_dist == sys.maxsize:
                # Not part of loop, determine if inside or outside
                if (mode):
                    inside_count += 1
                    node.mode = 'I'
                else:
                    outside_count += 1
                    node.mode = 'O'
                continue

            # Node is part of the loop
            node.mode = '.'
            pipe_count += 1
            t = node.type
            if t == '|':
                mode = 1 - mode
            elif t == '-':
                pass
            elif t == 'F':
                cur_type = t
            elif t == 'L':
                cur_type = t
            elif t == '7':
                if cur_type not in [ 'F', 'L' ]:
                    raise Exception(f"BAD CUR_TYPE {cur_type} for {t}")
                if cur_type == 'F':
                    pass
                elif cur_type == 'L':
                    mode = 1-mode
                cur_type = ''
            elif t == 'J':
                if cur_type not in [ 'F', 'L' ]:
                    raise Exception(f"BAD CUR_TYPE {cur_type} for {t}")
                if cur_type == 'F':
                    mode = 1-mode
                elif cur_type == 'L':
                    pass
                cur_type = ''

    #pipe_map.dump_mode()

    print(f"pipe_count = {pipe_count}, inside_count = {inside_count}, outside_count = {outside_count}")
    return inside_count

inside_count = main()
print(f"Inside count is {inside_count}")
