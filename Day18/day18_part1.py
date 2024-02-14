#!/usr/bin/python
"""Advent of Code 2023, Day 18, Part 1

https://adventofcode.com/2023/day/18

Give a list of vertical/horizontal moves of a digging machine, calculate the
total area enclosed by the path. Part 1 had a small region, so it just uses
an image and fill algorithm.

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

    # Create a rastor representation of the segments
    def make_raster(self):
        # First figure out dimensions of display
        min_x = 99999999
        min_y = 99999999
        max_x = -99999999
        max_y = -99999999
        for seg in self.seg_list:
            min_x = min(min_x, seg.x1, seg.x2)
            min_y = min(min_y, seg.y1, seg.y2)
            max_x = max(max_x, seg.x1, seg.x2)
            max_y = max(max_y, seg.y1, seg.y2)

        num_rows = (max_y - min_y)+1
        num_cols = (max_x - min_x)+1
        dsp_map = []
        for row in range(num_rows):
            dsp_map.append(bytearray('.' * num_cols, 'ascii'))

        for seg in self.seg_list:
            x1 = seg.x1
            x2 = seg.x2
            y1 = seg.y1
            y2 = seg.y2
            if x1 > x2:
                x1, x2 = x2, x1
            if y1 > y2:
                y1, y2 = y2, y1

            # Vertical
            marker = ord('#')
            if x1 == x2:
                for y in range(y1, y2+1):
                    dsp_map[y - min_y][x1 - min_x] = marker
            else:
                for x in range(x1, x2+1):
                    dsp_map[y1 - min_y][x - min_x] = marker

        return dsp_map

    # Create raster version of map and display
    def dump_map(self):
        raster = self.make_raster()
        self.dsp_raster(raster)

    # Display raster version of map
    def dsp_raster(self, raster):
        for row in raster:
            print(row.decode('ascii'))

    # Flood fill an enclosed raster image
    def flood_fill(self, raster, start_x, start_y):
        bc = ord('#')
        fc = ord('X')

        stack = [ (start_x, start_y) ]
        while stack:
            x, y = stack.pop()
            if raster[y][x] == bc or raster[y][x] == fc:
                continue

            raster[y][x] = fc
            if x > 0:
                stack.append((x-1, y))
            if x < len(raster[0])-1:
                stack.append((x+1, y))
            if y > 0:
                stack.append((x, y-1))
            if y < len(raster)-1:
                stack.append((x, y+1))

    # Find an interior point for the fill algorithm
    def find_interior_point(self, image):
        for y in range(len(image)):
            if image[y][0] == ord('#'):
                if image[y][1] == ord('.'):
                    return (1, y)

    # Calculate area
    def calc_area(self):
        image = self.make_raster()
        num_rows, num_cols = len(image), len(image[0])
        marker = ord('#')

        # Figure out any interior point
        x, y = self.find_interior_point(image)

        # Do flood fill
        self.flood_fill(image, x, y)
        #self.dsp_raster(image)

        # Count up the region filled
        area = 0
        for y in range(len(image)):
            for x in range(len(image[0])):
                if image[y][x] != ord('.'):
                    area += 1

        return area

#
# Main processing.
#
def main():
    # Read in all the entries

    dig_map = DigMap()
    cur_x = 0
    cur_y = 0
    with open(fn, 'r') as file:
        for line in file:
            line = line.rstrip('\n')

            matches = re.findall(r'(.) (\d+) \(#(.{6})', line)
            d = matches[0][0]
            steps = int(matches[0][1])

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

    #dig_map.dump_map()
    area = dig_map.calc_area()

    return area

area = main()
print(f"Total area is {area}")
