#!/usr/bin/python
"""Advent of Code 2023, Day 5, Part 1

https://adventofcode.com/2023/day/5

Translate "seed numbers" using translation map, and figuring out lowest
location code.

See test.dat for sample data and seeds.dat for full data.

Author: Tim Behrendsen
"""

import re
import sys

fn = 'seeds.dat'

# Dictionary to store mappings
mappings = { }


# Class for holding an entry within a Mapping
class Entry:
    def __init__(self, dest_start, src_start, length):
        self.dest_start = int(dest_start)
        self.src_start = int(src_start)
        self.length = int(length)

    # Check if seed_num is within the range, and return translated number. If not part of the range, return None.
    def translate(self, seed_num):
        # If within the range, then return new number at same difference from the destination as the source.
        if self.src_start <= seed_num < self.src_start + self.length:
            return seed_num - self.src_start + self.dest_start
        return None

# Class for holding a mapping of one type to another type
class Mapping:
    def __init__(self, src_name, dest_name):
        self.src_name = src_name
        self.dest_name = dest_name

        # List of entries for this mapping
        self.entry_list = []

    def add(self, dest_start, src_start, length):
        self.entry_list.append(Entry(dest_start, src_start, length))

    def translate(self, seed_num):
        for entry in self.entry_list:
            chk = entry.translate(seed_num)
            if (chk != None):
                return chk

        # If not found, use same seed number
        return seed_num


# Read seed data and mapping
with open(fn, 'r') as file:
    # Read list of seed numbers
    line = file.readline()
    seed_nums = re.findall(r'\d+', line)
    for i in range(len(seed_nums)):
        seed_nums[i] = int(seed_nums[i])

    line = file.readline()
    while line:
        line = line.rstrip('\n')

        # If line break, reset for new map
        if (line == ''):
            line = file.readline()
            line = line.rstrip('\n')
            matches = re.findall(r'(\w+)-to-(\w+) map', line)

            from_cat = matches[0][0]
            to_cat = matches[0][1]
            map = Mapping(from_cat, to_cat)

            mappings[from_cat] = map
        else:
            # Add new entry
            matches = re.findall(r'\d+', line)
            map.add(int(matches[0]), int(matches[1]), int(matches[2]))

        line = file.readline()

lowest = sys.maxsize
for seed_num in seed_nums:
    cur_src = "seed"
    num = seed_num
    while cur_src != "location":
        map = mappings[cur_src]
        new_num = map.translate(num)
        cur_src = map.dest_name
        num = new_num

    lowest = min(lowest, num)

print(f"Lowest is {lowest}")
