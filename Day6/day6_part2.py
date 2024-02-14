#!/usr/bin/python
"""Advent of Code 2023, Day 6, Part 2

https://adventofcode.com/2023/day/6

A boat has a button, where the longer you press it, the faster it goes. Calculate
how far the boat will go out different time scenarios to optimize the distance.
In part2, the numbers from the data are appended to give much larger numbers that
needed a more complex approach.

The nature of the time scenarios is that there was an optimal number and we
needed to know how many of those are above a threshhold. Rather than brute-forcing
testing every number, it does a pseudo-binary-search to do a gradient descent on
both sides of the curve to locate the crossover point. After calculate the ends,
the difference is the number of time scenarios that are above the distance
threshhold.

See test.dat for sample data and race.dat for full data.

Author: Tim Behrendsen
"""

import re

fn = 'test.dat'
fn = 'race.dat'

#
# Calculate distance based on when we press the button
#
def calc_dist(race, tm):
    speed = tm
    time_left = race['time'] - tm;
    return speed * time_left

#
# Do pseudo-binary search gradient descent to locate crossover point where we start breaking the record
#
def find_crossover(race, t_low, t_high):
    while (abs(t_low - t_high) > 1):
        mid = int((t_low + t_high) / 2)

        # Figure out which way is best and descend the gradient toward the crossover point
        mid_low = int((t_low + mid) / 2)
        dist_low = calc_dist(race, mid_low)
        diff_low = abs(dist_low - race['dist'])
        if diff_low == 0:
            mid = mid_low
            break

        mid_high = int((t_high + mid) / 2)
        dist_high = calc_dist(race, mid_high)
        diff_high = abs(dist_high - race['dist'])
        if diff_high == 0:
            mid = mid_high
            break

        if diff_low < diff_high:
            t_high = mid
        else:
            t_low = mid

    return t_low

# Read race data
with open(fn, 'r') as file:
    # Read list of times
    line = file.readline()
    line = re.sub('\s+', '', line)
    matches = re.findall(r'\d+', line)
    tm = int(matches[0])

    # Read time and distance
    line = file.readline()
    line = re.sub('\s+', '', line)
    matches = re.findall(r'\d+', line)
    dist = int(matches[0])

    race = { 'time': tm, 'dist': dist }

    t_low = 0
    tm = race['time']

    # Find low crossover point
    n1 = find_crossover(race, 0, int(tm / 2))

    # Find high crossover point
    n2 = find_crossover(race, int(tm / 2), tm)

    # We might be off by one, but we'll do 5 just in case. Look for exact record points.
    chk1 = n1-5
    while True:
        dist = calc_dist(race, chk1)
        if dist > race['dist']:
            break
        chk1 += 1

    chk2 = n2+5
    while True:
        dist = calc_dist(race, chk2)
        if dist > race['dist']:
            break
        chk2 -= 1
    chk2 += 1

    # Answer is the difference
    print(f"Number of record setting time values: {chk2 - chk1}")
