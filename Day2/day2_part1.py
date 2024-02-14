#!/usr/bin/python
"""Advent of Code 2023, Day 2, Part 1

https://adventofcode.com/2023/day/2

Game of drawing colored cubes from a bag. Figure out what games are possible if the
number of colors is limited to a certain count.

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

        color_count = { 'red': 0, 'green': 0, 'blue': 0 }
        is_poss = True

        for game in game_list:
            rounds = re.findall('(\d+) (\w+)', game)
            for round in rounds:
                if (int(round[0]) > max_count[round[1]]):
                    is_poss = False
                    break
            if (not is_poss):
                break

        if (is_poss):
            total += int(game_num)


print(f"Total of possible game IDs: {total}")
