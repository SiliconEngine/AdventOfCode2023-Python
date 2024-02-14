#!/usr/bin/python
"""Advent of Code 2023, Day 6, Part 1

https://adventofcode.com/2023/day/6

A boat has a button, where the longer you press it, the faster it goes. Calculate
how far the boat will go out different time scenarios to optimize the distance.
Calculate how many scenarios break the "distance record" in the sample data, and
multiply them together.

See test.dat for sample data and race.dat for full data.

Author: Tim Behrendsen
"""

import re
import sys
from functools import reduce

fn = 'test.dat'
fn = 'race.dat'

# Read race data
with open(fn, 'r') as file:
    # Read list of times
    line = file.readline()
    matches = re.findall(r'\d+', line)
    times = []
    for n in matches:
        times.append(int(n))

    # Read list of times and max distances
    line = file.readline()
    matches = re.findall(r'\d+', line)
    dists = []
    for n in matches:
        dists.append(int(n))

    records = []
    for i in range(len(times)):
        records.append({ 'time': times[i], 'dist': dists[i] })

    beaten_counts = []
    for race in records:
        beat_count = 0
        for t in range(1, race['time']):
            speed = t
            time_left = race['time'] - t;
            dist = speed * time_left
            if (dist > race['dist']):
                beat_count += 1

        beaten_counts.append(beat_count)

    prod = reduce(lambda x, y: x * y, beaten_counts)

    print(f"Number of records beaten, multiplied together: {prod}")

