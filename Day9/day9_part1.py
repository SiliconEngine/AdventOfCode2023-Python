#!/usr/bin/python
"""Advent of Code 2023, Day 9, Part 1

https://adventofcode.com/2023/day/9

Give a list of numbers, predict the next number in the sequence by the following
algorithm: Calculate the difference between each pair of numbers, creating a new
list. If contains all zeroes, then stop, otherwise continue the reduction. When
all zeroes, add a zero to the end, then add a new entry to the prior lists,
continuing back until the original list, and then taking the new number.

See test.dat for sample data and porert.dat for full data.

Author: Tim Behrendsen
"""

import re

fn = 'test.dat'
fn = 'test2.dat'
fn = 'report.dat'

def predict(seq):
    seq_list = [ seq.copy() ]
    cur_seq = seq.copy()
    while True:
        next_seq = []
        has_nonzero = False
        for idx in range(0, len(cur_seq)-1):
            diff = cur_seq[idx+1] - cur_seq[idx]
            next_seq.append(diff)
            if (diff != 0):
                has_nonzero = True

        seq_list.append(next_seq.copy())
        cur_seq = next_seq.copy()

        if (not has_nonzero):
            break

    print(seq_list)
    seq_list[-1].append(0)
    print(seq_list)

    for idx in range(len(seq_list)-2, -1, -1):
        prior_seq = seq_list[idx+1]
        cur_seq = seq_list[idx]
        cur_seq.append(prior_seq[-1] + cur_seq[-1])

    print(seq_list)

    return seq_list[0][-1]

def main():
    # Read each list of numbers and calculate the predicted next number
    node_map = { }
    total = 0
    with open(fn, 'r') as file:
        for line in file:
            seq = re.findall(r'-?\d+', line)
            seq = [ int(item) for item in seq ]
            print(seq)

            # Get the next sequence and total it up
            new_seq = predict(seq)
            print(f"New sequence is {new_seq}")
            total += new_seq

    return total

total = main()
print(f"Total extrapolated values is {total}")
