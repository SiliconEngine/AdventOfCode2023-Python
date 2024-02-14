#!/usr/bin/python
"""Advent of Code 2023, Day 24, Part 2

https://adventofcode.com/2023/day/24

Given 3D coordinates and velocities of "hailstones", figure out a rock that
if throws from 3D integer coordinates at 3D integer velocities, will intersect
with all given hailstones.

This was a tricky problem, which was solved using that we know things are
integers and so we can find pairs of stones that have the same X, Y, or Z
velocity. If they have the same velocity, then we know they stay the same
distance on the axis, and so the intercepting rock's velocity has to be a
factor of the gap distance.

We build a list of candidate velocities, then find a common factor among all
the candidates of all the pairs. We do this for X, Y, and Z, and this
produces the final velocity. Working backward from a pair of hailstones
gives the origin X, Y, Z.

This solution doesn't work with the test data, because there aren't enough
points with the same delta number, so we can't use that trick.

See test.dat for sample data and paths.dat for full data.

Author: Tim Behrendsen
"""

import re
import sys
import itertools as it

fn = 'test.dat'
fn = 'paths.dat'

class Hailstone:
    def __init__(self, x, y, z, dx, dy, dz):
        self.x, self.y, self.z = int(x), int(y), int(z)
        self.dx, self.dy, self.dz = int(dx), int(dy), int(dz)

    def __repr__(self):
        return f"[{self.x}, {self.y}, {self.z} / {self.dx}, {self.dy}, {self.dz}]"

    def unpack(self):
        return self.x, self.y, self.z, self.dx, self.dy, self.dz

#
# Return factors for number less than 1000
#
def factor_lt_1000(n):
    n = abs(n)
    factors = set()
    for i in range(1, min(1000, int(n ** 0.5) + 1)):
        if n % i == 0:
            factors.add(i)
            i2 = n // i
            if i2 < 1000:
                factors.add(i2)

    return sorted(factors)

#
# Main processing.
#
def main():
    # Read in all the maps, each as an array of strings
    stone_list = []
    with open(fn, 'r') as file:
        for line in file:
            line = line.rstrip('\n')
            matches = re.findall(r'(-?\d+)', line)
            stone = Hailstone(*matches)
            stone_list.append(stone)

    # Potential dx/dy/dz for the thrown rock
    pot_dx_set = None
    pot_dy_set = None
    pot_dz_set = None
    for A, B in it.combinations(stone_list, 2):
        ax, ay, az, adx, ady, adz = A.unpack()
        bx, by, bz, bdx, bdy, bdz = B.unpack()

        # If both A and B have same x velocity
        if adx == bdx:
            # Gap amount between A and B X coordinates will be a constant
            x_diff = bx - ax

            # EXAMPLE
            #     GAP = 105 (gap between these two will always be this amount)
            #     dx = 10   (so these points are moving in sync by 10 each time)
            #
            #     Factors of 105 = 1, 3, 5, 7, 15, 21, 35, 105
            #     Potential rock solutions have to make up the gap of 105 between
            #     this pair, and also account for base velocity of 10. Making up
            #     the gap can be done with some multiple of the factors.
            #
            #     So we know that for this pair of rocks, the dx for the final
            #     solution must be one dx +/- [factor].
            #
            #     We only check factors < 1000 since that was all that's required
            #     for the solution and speeds things up. Note that the hailstone
            #     velocities are < 1000.
            #
            new_x_set = set()
            for f in factor_lt_1000(x_diff):
                new_x_set.add(adx + f)
                new_x_set.add(adx - f)

            if pot_dx_set != None:
                pot_dx_set &= new_x_set         # Keep ones in common
            else:
                pot_dx_set = new_x_set

            #print(f"dx = {adx}, x_diff = {x_diff}, factors={factors}, new_x_set = {new_x_set}")
            #print(f"    pot_dx_set = {pot_dx_set}")

        if ady == bdy:
            y_diff = by - ay

            new_y_set = set()
            for f in factor_lt_1000(y_diff):
                new_y_set.add(ady + f)
                new_y_set.add(ady - f)

            if pot_dy_set != None:
                pot_dy_set &= new_y_set
            else:
                pot_dy_set = new_y_set

            #print(f"dy = {ady}, y_diff = {y_diff}, factors={factors}, new_y_set = {new_y_set}")
            #print(f"    pot_dy_set = {pot_dy_set}")

        if adz == bdz:
            z_diff = bz - az

            new_z_set = set()
            for f in factor_lt_1000(z_diff):
                new_z_set.add(adz + f)
                new_z_set.add(adz - f)

            if pot_dz_set != None:
                pot_dz_set &= new_z_set
            else:
                pot_dz_set = new_z_set

            #print(f"dz = {adz}, z_diff = {z_diff}, factors={factors}, new_z_set = {new_z_set}")
            #print(f"    pot_dz_set = {pot_dz_set}")

    print(pot_dx_set, pot_dy_set, pot_dz_set)
    rdx, rdy, rdz = pot_dx_set.pop(), pot_dy_set.pop(), pot_dz_set.pop()

    # Work backwards from the first two stones to calculate starting position
    ax, ay, az, adx, ady, adz = stone_list[0].unpack()
    bx, by, bz, bdx, bdy, bdz = stone_list[1].unpack()

    ma = (ady - rdy) / (adx - rdx)
    mb = (bdy - rdy) / (bdx - rdx)
    ca = ay - (ma * ax)
    cb = by - (mb * bx)
    xpos = round((cb - ca) / (ma - mb))
    ypos = round(ma * xpos + ca)
    t = (xpos - ax) // (adx - rdx)
    zpos = az + (adz - rdz) * t

    print(xpos, ypos, zpos)
    answer = xpos + ypos + zpos

    return answer

answer = main()
print(f"Answer is {answer}")
