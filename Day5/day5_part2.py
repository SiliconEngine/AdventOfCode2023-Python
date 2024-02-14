#!/usr/bin/python
"""Advent of Code 2023, Day 5, Part 2

https://adventofcode.com/2023/day/5

Translate "seed numbers" using translation map, and figuring out lowest
location code. For part 2, the seed numbers are ranges, and the ranges are
too large to use brute force with the full puzzle data, so you have to
process them as range pairs, splitting the ranges as needed when scanning
the translation maps.

See test.dat for sample data and seeds.dat for full data.

Author: Tim Behrendsen
"""

import re
import sys

fn = 'seeds.dat'

# Dictionary to store mappings
mappings = { }

# Maximum category number, so we can fill out the gaps
max_cat_num = 0

#
# Class for holding an entry within a Mapping
#
class Entry:
    def __init__(self, dest_start, src_start, length):
        self.dest_start = int(dest_start)
        self.src_start = int(src_start)
        self.length = int(length)
        self.range = (src_start, src_start+length-1)

        # Amount to add to translate from one to the other
        self.tran_diff = self.dest_start - self.src_start

    def __str__(self):
        return f"[range: {self.range[0]} - {self.range[1]}, diff={self.tran_diff}]"

    def __repr__(self):
        return self.__str__()

#
# Class for holding a mapping of one type to another type
#
class Mapping:
    def __init__(self, src_name, dest_name):
        self.src_name = src_name
        self.dest_name = dest_name

        # List of entries for this mapping
        self.entry_list = []

    # Add new entry
    def add(self, dest_start, src_start, length):
        self.entry_list.append(Entry(dest_start, src_start, length))

    # Scan completed range list and fill out gaps with ranges that will give the same number
    def fill_gaps(self):
        # First make sure the range list is sorted
        self.entry_list.sort(key=lambda entry: entry.src_start)

        # Add range at front and range at end
        if self.entry_list[0].range[0] > 0:
            self.entry_list.insert(0, Entry(0, 0, self.entry_list[0].range[0]))

        if self.entry_list[-1].range[1] < max_cat_num:
            n = self.entry_list[-1].range[1]
            self.entry_list.append(Entry(n+1, n+1, max_cat_num-n))

        # Find gaps and add ranges to just give same seed value
        i = 0
        while i < len(self.entry_list)-1:
            entry1 = self.entry_list[i]
            entry2 = self.entry_list[i+1]
            diff = entry2.range[0] - entry1.range[1]
            if (diff != 1):
                n1 = entry1.range[1]
                n2 = entry2.range[0]
                self.entry_list.insert(i+1, Entry(n1, n1, n2-n1))

            i += 1

    def translate(self, cat_set):
        new_cat_set = []
        for r in cat_set:
            low = r[0]
            high = r[1]

            for entry in self.entry_list:
                # Check if range is within this entry
                if not (high < entry.range[0] or low > entry.range[1]):
                    # Is low/high completely within entry
                    if low >= entry.range[0] and high <= entry.range[1]:
                        new_cat_set.append((low + entry.tran_diff, high + entry.tran_diff))

                    # Is range completely within low/high: narrow to range
                    elif low < entry.range[0] and high > entry.range[1]:
                        new_cat_set.append((entry.range[0] + entry.tran_diff, entry.range[1] + entry.tran_diff))

                    # If low below range, need to split: entry.range[0] to high
                    elif low < entry.range[0]:
                        new_cat_set.append((entry.range[0] + entry.tran_diff, high + entry.tran_diff))

                    # If high above range, need to split: low to entry.range[1]
                    #else if high > entry.range[1]:
                    else:
                        new_cat_set.append((low + entry.tran_diff, entry.range[1] + entry.tran_diff))

        return new_cat_set

# Read seed data and mapping
with open(fn, 'r') as file:
    # Read list of seed numbers
    line = file.readline()
    seed_nums = re.findall(r'\d+', line)
    seed_ranges = []
    for i in range(0, len(seed_nums), 2):
        seed_num = int(seed_nums[i])
        seed_ranges.append( (seed_num, seed_num + int(seed_nums[i+1]) - 1) )

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
            cat_map = Mapping(from_cat, to_cat)

            mappings[from_cat] = cat_map
        else:
            # Add new entry
            matches = re.findall(r'\d+', line)
            dest_start = int(matches[0])
            src_start = int(matches[1])
            entry_len = int(matches[2])
            cat_map.add(dest_start, src_start, entry_len)
            max_cat_num = max(max_cat_num, dest_start + entry_len, src_start + entry_len)

        line = file.readline()

for cat_map in mappings.values():
    cat_map.fill_gaps()

lowest = sys.maxsize
for seed_range in seed_ranges:

    cat_set = [ seed_range ]
    cur_src = "seed"
    while cur_src != "location":
        cat_map = mappings[cur_src]
        new_cat_set = cat_map.translate(cat_set)
        cur_src = cat_map.dest_name
        cat_set = new_cat_set

    # Find lowest in set of ranges
    for r in cat_set:
        lowest = min(lowest, r[0])

print(f"Lowest is {lowest}")
