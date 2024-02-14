#!/usr/bin/python
"""Advent of Code 2023, Day 2, Part 2

https://adventofcode.com/2023/day/2

Game of drawing colored cubes from a bag. Figure out minimum cubes needed
for each game, multiple the count together to produce the "power", then total
it up.

See test.dat for sample data and games.dat for full data.

Author: Tim Behrendsen
"""

import re

fn = 'games.dat'

max_count = { 'red': 12, 'green': 13, 'blue': 14 }
total = 0

with open(fn, 'r') as file:
    for line in file:
        line = line.rstrip('\n')
        matches = re.findall("Game (\d+): (.*)", line);
        game_num = matches[0][0]
        games = matches[0][1]
        game_list = games.split('; ')

        max_count = { 'red': 0, 'green': 0, 'blue': 0 }

        for game in game_list:
            rounds = re.findall('(\d+) (\w+)', game)

            for round in rounds:
                max_count[round[1]] = max(max_count[round[1]], int(round[0]))

        power = max_count['red'] * max_count['green'] * max_count['blue']
        total += power

print(f"Total cube power: {total}")
