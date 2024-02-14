#!/usr/bin/python
"""Advent of Code 2023, Day 18, Part 2

https://adventofcode.com/2023/day/18

Give a list of vertical/horizontal moves of a digging machine, calculate the
total area enclosed by the path. Part 2 has a much larger footprint, so needs
a more sophisticated algorithm.

It first uses the Shoelace Algorithm to calculate the area of the polygon given
the list of segments. However, the total needs to include the width of the path,
so also needs to add up all the outward facing edges on the right and on the
bottom. I used a clockwise algorithm to determine which side of the edge was facing
outward, and added up the missing squares.

The other way I could have done it was to use the clockwise method to adjust the
coordinates of the right/bottom outward facing edges so they'd be included in the
shoelace total, which might have been cleaner, but this got the right answer.

See test.dat for sample data and plan.dat for full data.

Author: Tim Behrendsen
"""

import re
import sys

fn = 'test.dat'
fn = 'plan.dat'

#
# Represent one segment of the path
#
class Segment:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __repr__(self):
        return f"[{self.x1}, {self.y1} -> {self.x2}, {self.y2}]"

#
# Digging map
#
class DigMap:
    def __init__(self):
        self.seg_list = []

    # Add a segment to map
    def add_segment(self, x1, y1, x2, y2):
        seg = Segment(x1, y1, x2, y2)
        self.seg_list.append(seg)

    # Dump out segments and x, y ranges
    def dump_segs(self):
        # First figure out dimensions of display
        min_x = 999999999999
        min_y = 999999999999
        max_x = -999999999999
        max_y = -999999999999
        for seg in self.seg_list:
            print(f"Seg: {seg}")
            min_x = min(min_x, seg.x1, seg.x2)
            min_y = min(min_y, seg.y1, seg.y2)
            max_x = max(max_x, seg.x1, seg.x2)
            max_y = max(max_y, seg.y1, seg.y2)

        print(f"range is {min_x} to {max_x} ({max_x - min_x + 1}), {min_y} to {max_y} ({max_y - min_y + 1})")

    # Calculate area using shoelace formula
    def calc_area(self):
        area = 0.0
        n = len(self.seg_list)

        # Loop till the second last vertex
        for i in range(n - 1):
            j = (i + 1) % n
            area += self.seg_list[i].x1 * self.seg_list[j].y1
            area -= self.seg_list[j].x1 * self.seg_list[i].y1
        return abs(area) / 2

    # Identify outfacing edges and for the right-facing and bottom-facing
    # ones, figure out how many extra squares need to be added in
    def identify_outfacing(self):
        extra = 0
        extra_vertices = 0
        for idx in range(len(self.seg_list)):
            seg = self.seg_list[idx]
            if idx < len(self.seg_list)-1:
                next_seg = self.seg_list[idx+1]
            else:
                next_seg = self.seg_list[0]

            #print(f"{seg} :: {next_seg} ", end='')
            if seg.y1 == seg.y2:
                # Horizontal
                if seg.x2 > seg.x1:
                    # Left to right
                    if seg.y2 < next_seg.y1:
                        # Counter-clockwise, outward down, count this one
                        extra += seg.x2 - seg.x1
                        extra_vertices += 1
                    else:
                        # Clockwise, outward up
                        pass
                else:
                    # Right to left
                    if seg.y2 > next_seg.y1:
                        # Clockwise, outward up
                        pass
                    else:
                        # Counter-clockwise, outward down, count this one
                        extra += seg.x1 - seg.x2
                        extra_vertices += 1
            else:
                # Vertical
                if seg.y2 > seg.y1:
                    # North to south
                    if seg.x2 < next_seg.x1:
                        # Counter-clockwise, outward left
                        pass
                    else:
                        # Clockwise, outward right, count this one
                        extra += seg.y2 - seg.y1
                        extra_vertices += 1
                else:
                    # South to north
                    if seg.x2 > next_seg.x1:
                        # Clockwise, outward right, count this one
                        extra += seg.y1 - seg.y2
                        extra_vertices += 1
                    else:
                        # Counter-clockwise, outward left
                        pass

        return extra

#
# Main processing.
#
def main():
    # Read in all the entries

    dirs = {
        '0': 'R',
        '1': 'D',
        '2': 'L',
        '3': 'U',
    }

    dig_map = DigMap()
    cur_x = 0
    cur_y = 0
    with open(fn, 'r') as file:
        for line in file:
            line = line.rstrip('\n')

            matches = re.findall(r'(.) (\d+) \(#(.{6})', line)
            steps = int(matches[0][2][0:5], 16)
            d = dirs[matches[0][2][5]]

            x2 = cur_x
            y2 = cur_y

            if d == 'U':
                y2 -= steps
            elif d == 'D':
                y2 += steps
            elif d == 'L':
                x2 -= steps
            elif d == 'R':
                x2 += steps

            dig_map.add_segment(cur_x, cur_y, x2, y2)
            cur_x = x2
            cur_y = y2

    #dig_map.dump_segs()

    # Calculate basic area of the shape
    area = dig_map.calc_area()

    # Need to include the outfacing edges on the right and on the
    # bottom, which didn't get included  in the shoelace calculation.
    extra = dig_map.identify_outfacing()

    # Plus one for the final uncounted vertex
    return area + extra + 1

area = main()
print(f"Total area is {area}")
