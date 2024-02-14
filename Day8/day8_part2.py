#!/usr/bin/python
"""Advent of Code 2023, Day 8, Part 2

https://adventofcode.com/2023/day/8

Follow the path of a node map by moving right / left. In this case, we start
at all nodes that end with A and move to a node that ends with Z. But we only
stop when all paths end on a Z.

It turns out that the general solution takes an impractical number of steps,
but the puzzle data ends up having regular patterns. We can shortcut the
calculation by figuring out the pattern, then doing a Least Common Multiple
of the repeating numbers.

See test2.dat for sample data and nav.dat for full data.

Author: Tim Behrendsen
"""

import re
import math

fn = 'test2.dat'
fn = 'nav.dat'

def main():
    # Read card hands and build list with classification
    node_map = { }
    start_nodes = []

    with open(fn, 'r') as file:

        # Get list of left/right movement
        movement = file.readline()
        movement = movement.rstrip('\n')

        # Read node maps, after skipping blank line
        line = file.readline()
        line = file.readline()
        while (line):
            matches = re.findall(r'(\w\w\w) = .(\w+), (\w+)', line)
            node = matches[0][0]
            node_map[node] = { 'left': matches[0][1], 'right': matches[0][2] }

            # Find all start nodes that end in 'A'
            line = file.readline()
            if (node[-1] == 'A'):
                start_nodes.append(node)

    steps = 0
    cur_nodes = start_nodes.copy()
    cycle_list = {}
    for node in start_nodes:
        cycle_list[node] = []

    while True:
        for dir in movement:
            z_count = 0
            steps += 1
            # After 100K steps, terminate and figure out the patterns. In theory
            # we could terminate after accumulating enough cycle data.
            if (steps % 100000 == 0):
                return cycle_list

            for idx in range(len(cur_nodes)):
                cur_node = cur_nodes[idx]

                if (dir == 'L'):
                    cur_node = node_map[cur_node]['left']
                else:
                    cur_node = node_map[cur_node]['right']
                cur_nodes[idx] = cur_node

                if cur_node[-1] == 'Z':
                    z_count += 1
                    cycle_list[start_nodes[idx]].append(steps)

            # If it was practical to run the whole thing, this would terminate with
            # the answer
            if z_count == len(start_nodes):
                print(f"Number of steps is {steps}")
                exit(0)


# For this narrow solution, we just get the cycles
cycle_list = main()

# Verify cycles are consistent and accumulate difference values
diff_list = { }
for node, cycles in cycle_list.items():
    last_num = 0
    last_diff = -1
    for num in cycles:
        diff = num - last_num
        last_num = num
        if (last_diff > 0 and diff != last_diff):
            raise Exception(f"ERROR: last_diff was {last_diff}, diff was {diff}")
        last_diff = diff

    diff_list[node] = last_diff

# Calculate Least Common Multiple of difference values for shortcut to number of steps
diff_values = list(diff_list.values())
cur_num = diff_values[0]
for idx in range(1, len(diff_list)):
    next_num = diff_values[idx]
    lcm = (cur_num * next_num) / math.gcd(cur_num, next_num)
    cur_num = int(lcm)

steps = cur_num
print(f"Number of steps is {steps}")
