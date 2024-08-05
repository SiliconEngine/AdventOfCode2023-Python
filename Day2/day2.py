#!/usr/bin/python
"""Advent of Code 2023, Day 2

https://adventofcode.com/2023/day/2

Game of drawing colored cubes from a bag. In part 1, figure out what games are
possible if the number of colors is limited to a certain count.

In part 2, figure out minimum cubes needed for each game, multiple the count
together to produce the "power", then total it up.

See test.dat for sample data and games.dat for full data.

Author: Tim Behrendsen
"""

import re
fn = 'games.dat'

# Generate game number + list of games
def gen_games(lines):
    for line in lines:
        matches = re.findall("Game (\d+): (.*)", line)[0]
        game_num, game_list = matches[0], matches[1].split('; ')
        yield game_num, game_list

def part1(lines):
    total = 0
    max_count = { 'red': 12, 'green': 13, 'blue': 14 }
    for game_num, game_list in gen_games(lines):
        color_count = { 'red': 0, 'green': 0, 'blue': 0 }
        is_poss = any(int(round[0]) > max_count[round[1]]
            for game in game_list for round in re.findall('(\d+) (\w+)', game))
        if (is_poss):
            total += int(game_num)

    return total

def part2(lines):
    total = 0
    for game_num, game_list in gen_games(lines):
        count = { 'red': 0, 'green': 0, 'blue': 0 }
        for game in game_list:
            rounds = re.findall('(\d+) (\w+)', game)
            for round in rounds:
                count[round[1]] = max(count[round[1]], int(round[0]))

        power = count['red'] * count['green'] * count['blue']
        total += power

    return total

lines = [ line.strip() for line in open(fn, 'r') ]
print(f"Total of possible game IDs: {part1(lines)}")
print(f"Total cube power: {part2(lines)}")
