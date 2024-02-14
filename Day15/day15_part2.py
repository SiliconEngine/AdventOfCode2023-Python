#!/usr/bin/python
"""Advent of Code 2023, Day 15, Part 2

https://adventofcode.com/2023/day/15

Given a list of lens tags and lens numbers, apply the operation code (- or =) to
place each one in a set of boxes, each of which may contains multiple lenses.
Process each command, then total up the "focusing power" based on their box
numbers and lens numbers.

See test.dat for sample data and sequence.dat for full data.

Author: Tim Behrendsen
"""

import re
import sys

fn = 'test.dat'
fn = 'sequence.dat'

#
# Calculate hash code according to puzzle algorithm
#
def calc_hash(s):
    val = 0
    for c in s:
        val += ord(c)
        val *= 17
        val = val % 256

    return val

def dump_boxes(boxes):
    for i in range(0, 255):
        if len(boxes[i]) > 0:
            print(f"Box {i}: ", end='')
            for lens in boxes[i]:
                print(f" [{lens[0]} {lens[1]}]", end='')
            print('')

#
# Main processing.
#
def main():
    # Read in all the maps, each as an array of strings
    total = 0
    with open(fn, 'r') as file:
        seq = file.readline()
        seq = seq.rstrip('\n')

    boxes = []
    for i in range(0, 256):
        boxes.append([])

    s_list = seq.split(',')
    for s in s_list:
        matches = re.findall(r'(\w+)(-|=)(\d*)', s)
        label = matches[0][0]
        op = matches[0][1]
        box = calc_hash(label)
        lens = matches[0][2]

        if op == '-':
            # Remove lens, if exists
            for idx in range(len(boxes[box])-1, -1, -1):
                if boxes[box][idx][0] == label:
                    del boxes[box][idx]

        else:
            # Add or replace lens in box
            had_lens = False
            for idx in range(len(boxes[box])-1, -1, -1):
                if boxes[box][idx][0] == label:
                    boxes[box][idx] = (label, lens)
                    had_lens = True
                    break

            if not had_lens:
                boxes[box].append((label, lens))

        #dump_boxes(boxes)

    # Add up "focusing power" using formula
    total = 0
    box_num = 0
    for box in boxes:
        slot = 0
        for lens in box:
            slot += 1
            total += (box_num+1) * slot * int(lens[1])

        box_num += 1

    return total

total = main()
print(f"Total of hash numbers is {total}")
