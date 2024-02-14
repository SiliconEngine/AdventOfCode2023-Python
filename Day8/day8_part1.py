#!/usr/bin/python
"""Advent of Code 2023, Day 8, Part 1

https://adventofcode.com/2023/day/8

Follow the path of a node map by moving right / left. Calculate number of steps
to from the AAA node to the ZZZ node.

See test.dat for sample data and nav.dat for full data.

Author: Tim Behrendsen
"""

import re

fn = 'test.dat'
fn = 'nav.dat'

def main():
    # Read card hands and build list with classification
    node_map = { }
    with open(fn, 'r') as file:

        # Get list of left/right movement
        movement = file.readline()
        movement = movement.rstrip('\n')

        # Read node maps, after skipping blank line
        line = file.readline()
        line = file.readline()
        while (line):
            matches = re.findall(r'(\w\w\w) = .(\w+), (\w+)', line)
            node_map[matches[0][0]] = { 'left': matches[0][1], 'right': matches[0][2] }
            line = file.readline()

    steps = 0
    cur_node = 'AAA'
    while True:
        for dir in movement:
            steps += 1
            if (dir == 'L'):
                cur_node = node_map[cur_node]['left']
            else:
                cur_node = node_map[cur_node]['right']

            if (cur_node == 'ZZZ'):
                return steps


steps = main()
print(f"Number of steps is {steps}")
