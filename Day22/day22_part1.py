#!/usr/bin/python
"""Advent of Code 2023, Day 22, Part 1

https://adventofcode.com/2023/day/22

Given a list of falling three dimensional bricks, simulate them reaching
the ground and stacking. Then figure out how many bricks can safely be
"disintegrated" without another brick falling (in other words, not supporting
another brick).

See test.dat for sample data and bricks.dat for full data.

Author: Tim Behrendsen
"""

import re
import sys

fn = 'test.dat'
fn = 'bricks.dat'

class Coord:
    def __init__(self, x, y, z):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)

    def __repr__(self):
        return f"[{self.x}, {self.y}, {self.z}]"

class Brick:
    def __init__(self, c1, c2, id):
        self.supporting = []
        self.under_list = []
        self.id = id

        # Coordinates will always be in 'z' order, lowest first, then by x and y
        if c1.z < c2.z:
            self.coords = [ c1, c2 ]
            return
        if c1.z > c2.z:
            self.coords = [ c2, c1 ]
            return

        if c1.x < c2.x:
            self.coords = [ c1, c2 ]
            return
        if c1.x > c2.x:
            self.coords = [ c2, c1 ]
            return

        if c1.y < c2.y:
            self.coords = [ c1, c2 ]
        else:
            self.coords = [ c2, c1 ]
        return

    def __repr__(self):
        x = self.coords[0].x
        if x != self.coords[1].x:
            x = f"{x}-{self.coords[1].x}"
        y = self.coords[0].y
        if y != self.coords[1].y:
            y = f"{y}-{self.coords[1].y}"
        z = self.coords[0].z
        if z != self.coords[1].z:
            z = f"{z}-{self.coords[1].z}"

        return f"[{self.id}:{x}, {y}, {z}]"

    # Check if self brick is completely below given brick
    def below(self, brick):
        # Is self highest z below brick lowest z
        return self.coords[1].z < brick.coords[0].z

    # Check if self intersects with given brick
    def intersects(self, brick):
        def is_int(a1, a2, b1, b2):
            return a1 <= b2 and b1 <= a2

        x_int = is_int(self.coords[0].x, self.coords[1].x,
            brick.coords[0].x, brick.coords[1].x)
        y_int = is_int(self.coords[0].y, self.coords[1].y,
            brick.coords[0].y, brick.coords[1].y)
        z_int = is_int(self.coords[0].z, self.coords[1].z,
            brick.coords[0].z, brick.coords[1].z)
        return x_int and y_int and z_int

#
# Move bricks down by one, checking for collisions
# Returns True if any bricks moved
#
def move_bricks_down(brick_list):
    # First sort bricks by 'z'
    brick_list.sort(key=lambda b: b.coords[0].z)
    move_count = 0

    # Calculate the maximum size of a brick on the z axis. Needed
    # to know max distance we have to check
    max_z = 0
    for brick in brick_list:
        max_z = max(max_z, brick.coords[1].z - brick.coords[0].z + 1)

    # Start moving from the bottom
    for idx in range(len(brick_list)):
        brick = brick_list[idx]

        # Already on ground?
        if brick.coords[0].z == 1:
            continue

        # Do tentative move of brick
        brick.coords[0].z -= 1
        brick.coords[1].z -= 1

        # Check collision with rest of bricks below us
        # Search up and down our list, since we're sorted by z
        idx_stop = len(brick_list)
        for idx_stop in range(idx+1, len(brick_list)):
            brick2 = brick_list[idx_stop]
            if brick.below(brick2):
                break

        # Check for collisions with bricks at same level
        collision = False
        #for idx_chk in range(0, idx_stop):
        for idx_chk in range(min(idx_stop, len(brick_list)-1), -1, -1):
            if idx_chk == idx:          # Skip ourselves
                continue
            chk_brick = brick_list[idx_chk]

            # If we've moved below our brick, we can stop
            if chk_brick.coords[1].z < brick.coords[0].z-max_z:
                break

            if brick.intersects(chk_brick):
                collision = True
                break

        # If collision, reverse the move, down as far as we can go
        if collision:
            brick.coords[0].z += 1
            brick.coords[1].z += 1
        else:
            move_count += 1

    return move_count != 0

#
# Generate an 'id' for the brick, just for debugging
#
def get_id(idx):
    id = ''
    n = idx
    while (n):
        id = chr(ord('A') + n % 26) + id
        n //= 26
    if id == '':
        id = 'A'

    return id

#
# Main processing.
#
def main():
    # Read in all the bricks
    brick_list = []
    with open(fn, 'r') as file:
        for line in file:
            m = re.findall('\d+', line)

            brick = Brick(Coord(m[0], m[1], m[2]), Coord(m[3], m[4], m[5]), get_id(len(brick_list)))
            brick_list.append(brick)

    # Keep moving bricks until none can move any longer
    moved = True
    while moved:
        moved = move_bricks_down(brick_list)

    # Build lists of what bricks are supporting other bricks, and
    # what bricks directly under other other bricks
    for idx in range(0, len(brick_list)):
        brick1 = brick_list[idx]
        brick1.coords[0].z += 1
        brick1.coords[1].z += 1

        for idx2 in range(idx+1, len(brick_list)):
            brick2 = brick_list[idx2]
            if brick1.intersects(brick2):
                brick1.supporting.append(brick2)
                brick2.under_list.append(brick1)

        brick1.coords[0].z -= 1
        brick1.coords[1].z -= 1

    # Finally count the number of safe bricks
    ok_count = 0
    for brick in brick_list:
        # Look at each brick being supported and see if it has
        # multiple supports
        ok = True
        for supp in brick.supporting:
            if len(supp.under_list) == 1:
                ok = False
                break

        if ok:
            ok_count += 1

    return ok_count

total = main()
print(f"Count is {total}")
