# Advent of Code 2023 solutions written in Python.
## Author: Tim Behrendsen

Link: https://adventofcode.com/2023/

Advent of Code is a series of puzzles over 25 days, each with a part 1 and
part 2. The difficulty roughly rises each day, with the later puzzles often
requiring some tricky algorithms to solve.

For these solutions, the various days are in separate directories. Day 25, as
traditional, is only a single part.

### Advent of Code 2023, Day 1

Link: https://adventofcode.com/2023/day/1

Read lines, find first digit and last digit, combine to a number, and total. See
test.dat for sample data and calibrate.dat for full data.

For part 2, a digit may be spelled out, except for 'zero'. The tricky part was
that you could have overlap, like "eighthree" should be 83, so had to use regex lookahead.

### Advent of Code 2023, Day 2

Link: https://adventofcode.com/2023/day/2

Game of drawing colored cubes from a bag. In part 1, figure out what games are
possible if the number of colors is limited to a certain count.

In part 2, figure out minimum cubes needed for each game, multiple the count
together to produce the "power", then total it up.

### Advent of Code 2023, Day 3

Link: https://adventofcode.com/2023/day/3

Read "schematic" grid of numbers and symbols. In part 1, add up any numbers (sequence of
digits) that are adjacent to a non-period symbol, including diagonally.

In part 2, asterisk symbols are "gears". For any gears that are adjacent to exactly two
numbers, including diagonally, multiple the numbers together to give a "gear ratio". Sum
these numbers together.

### Advent of Code 2023, Day 4

Link: https://adventofcode.com/2023/day/4

Part 1: Calculate score of scratcher tickets and total them up.

Part 2: Add up total number of scratcher cards, taking into account copying based
on the number of matching numbers of the prior cards.

### Advent of Code 2023, Day 5, Part 1

Link: https://adventofcode.com/2023/day/5

Translate "seed numbers" using translation map, and figuring out lowest
location code.

### Advent of Code 2023, Day 5, Part 2

Link: https://adventofcode.com/2023/day/5

Translate "seed numbers" using translation map, and figuring out lowest
location code. For part 2, the seed numbers are ranges, and the ranges are
too large to use brute force with the full puzzle data, so you have to
process them as range pairs, splitting the ranges as needed when scanning
the translation maps.

### Advent of Code 2023, Day 6, Part 1

Link: https://adventofcode.com/2023/day/6

A boat has a button, where the longer you press it, the faster it goes. Calculate
how far the boat will go out different time scenarios to optimize the distance.
Calculate how many scenarios break the "distance record" in the sample data, and
multiply them together.

### Advent of Code 2023, Day 6, Part 2

Link: https://adventofcode.com/2023/day/6

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

### Advent of Code 2023, Day 7

Link: https://adventofcode.com/2023/day/7

Give sets of five playing cards, figure the hand type and rank them by strength.
Finally calculate a winning score by multiplying the bid by the index. In part 2,
the 'J' is now a joker, instead of a jack.

If hands are equal type, then cards are compared in order to determine which hand
is the strongest.

### Advent of Code 2023, Day 8, Part 1

Link: https://adventofcode.com/2023/day/8

Follow the path of a node map by moving right / left. Calculate number of steps
to from the AAA node to the ZZZ node.

### Advent of Code 2023, Day 8, Part 2

Link: https://adventofcode.com/2023/day/8

Follow the path of a node map by moving right / left. In this case, we start
at all nodes that end with A and move to a node that ends with Z. But we only
stop when all paths end on a Z.

It turns out that the general solution takes an impractical number of steps,
but the puzzle data ends up having regular patterns. We can shortcut the
calculation by figuring out the pattern, then doing a Least Common Multiple
of the repeating numbers.

### Advent of Code 2023, Day 9, Part 1

Link: https://adventofcode.com/2023/day/9

Give a list of numbers, predict the next number in the sequence by the following
algorithm: Calculate the difference between each pair of numbers, creating a new
list. If contains all zeroes, then stop, otherwise continue the reduction. When
all zeroes, add a zero to the end, then add a new entry to the prior lists,
continuing back until the original list, and then taking the new number.

### Advent of Code 2023, Day 9, Part 2

Link: https://adventofcode.com/2023/day/9

Give a list of numbers, predict the prior number in the sequence by the following
algorithm: Calculate the difference between each pair of numbers, creating a new
list. If contains all zeroes, then stop, otherwise continue the reduction. When all
zeroes, add a zero to the front, then add a new entry to front of the prior lists,
continuing back until the original list, and then taking the new number.

### Advent of Code 2023, Day 10, Part 1

Link: https://adventofcode.com/2023/day/10

Given a series of pipes on a map and starting position, figure out what pipes
form a loop and return the furthest distance from the start. The starting position
is an unknown type of pipe. This implementation uses Dijkstra's Algorithm to figure
the distances.

### Advent of Code 2023, Day 10, Part 2

Link: https://adventofcode.com/2023/day/10

Given a series of pipes on a map and starting position, figure out what pipes
form a loop. Given the loop, then figure out how many nodes are fully enclosed
by the loop.

This implementation uses Dijkstra's Algorithm to figure the loop (from Part 1). Then
it uses the Even-Odd Rule to determine when each node is within the loop.

### Advent of Code 2023, Day 11

Link: https://adventofcode.com/2023/day/11

Given a map of galaxies, figure out the total of the taxi distance between each
pair of them. However, if there are rows without galaxies, each of those rows count
as two, and columns without galaxies also count as two. In part 2, each of those
rows count as one million, and columns without galaxies also count as one million.

### Advent of Code 2023, Day 12, Part 1

Link: https://adventofcode.com/2023/day/12

Given a pattern with missing information, figure out the number of combinations
that could potentially fit the set of numbers given (set of number of hashes in
a row).

This part 1 solution uses simple brute-force recursion.

### Advent of Code 2023, Day 12, Part 2

Link: https://adventofcode.com/2023/day/12

Given a pattern with missing information, figure out the number of combinations
that could potentially fit the set of numbers given (set of number of hashes in a row).
For part 2, the pattern is repeated four more times.

Because the patterns are much larger, brute-force becomes impractical. This algorithm
uses dynamic programming to cache parts of patterns so we can reuse that information
when we see common patterns.

### Advent of Code 2023, Day 13

Link: https://adventofcode.com/2023/day/13

Given a grid of '.' and '#' characters, find the reflection point that might be
vertical or horizontal. Total up the reflection rows / columns according to a formula.

In Part 2, exactly one character must be switched to find new reflections. Total up
the reflection rows / columns according to a formula.

### Advent of Code 2023, Day 14, Part 1

Link: https://adventofcode.com/2023/day/14

Given a grid of rocks, some rollable and some not, "tilt" the grid and roll the
rocks to the north. Afterward, calculate a "load number" using a formula.

### Advent of Code 2023, Day 14, Part 2

Link: https://adventofcode.com/2023/day/14

Given a grid of rocks, some rollable and some not, "tilt" the grid in each of
four directions, and roll the rocks in that direction. Repeat the cycle
1,000,000,000 times and calculate the final "load number" using a formula.

Required noticing the load number falls into a repeating pattern, so figures
out the pattern and calculates the 1,000,000,000 based on the pattern length.

### Advent of Code 2023, Day 15, Part 1

Link: https://adventofcode.com/2023/day/15

For part 1, given a list of strings, calculate the hash value using the given
algorithm and total it up.

For part 2, the strings are a list of lens tags and lens numbers. Apply the operation
code (- or =) to place each one in a set of boxes, each of which may contains multiple
lenses.  Process each command, then total up the "focusing power" based on their box
numbers and lens numbers.

### Advent of Code 2023, Day 16, Part 1

Link: https://adventofcode.com/2023/day/16

Given a grid of mirrors and prisms, track the reflected rays and count how many
tiles are crossed by light rays. If a prism, then light splits in two paths.
For part 2, we need to scan coming in from different directions to see which is
optimal.

Uses a recursive algorithm, plus a cache to detect if a path is being retraced
in the same direction

### Advent of Code 2023, Day 17

Link: https://adventofcode.com/2023/day/17

Given a map of heat values, calculate the optimal path to minimize the heat.
However, the path must follow these rules:

1) Start at upper left, and can either go south or east.
2) First node is not counted in heat total
3) Can move in same direction only a maximum of 3 moves
4) End at lower right.

Uses Dijkstra's Algorithm with a four dimensional graph of row, column,
direction and number of steps in that direction.

### Advent of Code 2023, Day 18, Part 1

Link: https://adventofcode.com/2023/day/18

Give a list of vertical/horizontal moves of a digging machine, calculate the
total area enclosed by the path. Part 1 had a small region, so it just uses
an image and fill algorithm.

### Advent of Code 2023, Day 18, Part 2

Link: https://adventofcode.com/2023/day/18

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

### Advent of Code 2023, Day 19, Part 1

Link: https://adventofcode.com/2023/day/19

Given a set of rules, process them for each "part" description, totaling
the "rating number" for the accepted parts.

### Advent of Code 2023, Day 19, Part 2

Link: https://adventofcode.com/2023/day/19

Given a set of rules that will produce either "Accept" or "Reject" for a part
based on its attributes, calculate the total number of combinations of part
numbers that will be accepted.

In part 1, we processed the rule for a specific part. This processes the
rules for a range of values, recursively checking different paths based on
the rules, and then totals of the combinations.

### Advent of Code 2023, Day 20, Part 1

Link: https://adventofcode.com/2023/day/20

Simulates a set of "modules" wired together that send signals in a certain
connected structure. Based on the rules of each module, totals up the number
of "low pulses" and "high pulses" and multiples them.

### Advent of Code 2023, Day 20, Part 2

Link: https://adventofcode.com/2023/day/20

Simulates a set of "modules" wired together that send signals in a certain
connected structure. For part 2, need to track the signal to 'rx' and predict
the fewest number of button presses required to recieve a low pulse.

This required looking back at the four "Conjunction" modules connected to 'rx'
and noticing that they have a repeating pattern. The repeating patterns turned
out to be four prime numbers, and it will only send the low pulse when each
of those triggered. So the code figures out the cycle times for each of
the four modules, and the product of the primes is the answer.

### Advent of Code 2023, Day 21, Part 1

Link: https://adventofcode.com/2023/day/21

Given a garden plot map and a starting point, compute how many garden plots can be
reached by walking an exact number of steps. Backtracking is allowed, so the
starting point would be reachable by stepping back and forth.

Uses a modified Dijkstra's Algorithm to complete the distances. The tricky part
is that any node reached with an even number of steps, from any direction,
qualifies as reachable.

### Advent of Code 2023, Day 21, Part 2

Link: https://adventofcode.com/2023/day/21

Given a garden plot map and a starting point, compute how many garden plots can be
reached by walking an exact number of steps. Backtracking is allowed, so the
starting point would be reachable by stepping back and forth.

Uses a modified Dijkstra's Algorithm to complete the distances. The tricky part
is that any node reached with an even number of steps, from any direction,
qualifies as reachable.

However, with Part 2, the garden is infinitely large by repeating the map pattern,
and we need to walk 26501365 steps.

There are a couple of key observations:
1) There is a repeating pattern of diamond shapes in the map.
2) 26501365 = 202300 * 131 + 65, and 131 is the size of the map.

It turns out that the step count follows a quadratic curve, and by calculating
the first few points, the formula can be fit to the data and then answer
computed.

The only last tricky part is that 26501365 is odd, so the progression
to be calculated needs to be odd numbers.

### Advent of Code 2023, Day 22, Part 1

Link: https://adventofcode.com/2023/day/22

Given a list of falling three dimensional bricks, simulate them reaching
the ground and stacking. Then figure out how many bricks can safely be
"disintegrated" without another brick falling (in other words, not supporting
another brick).

### Advent of Code 2023, Day 22, Part 2

Link: https://adventofcode.com/2023/day/22

Given a list of falling three dimensional bricks, simulate them reaching
the ground and stacking. Then for each brick, calculate how many would fall
if it was removed. Create a grand total.

This uses a recursive function to check each brick, marking them if they've
already been checked or if they're in the process of falling.

### Advent of Code 2023, Day 23, Part 1

Link: https://adventofcode.com/2023/day/23

Given a map of trails, compute the longest path, accounting for arrows that
restrict movements in certain directions, and you can't backtrack onto a tile
already visited. Uses a depth-first-search to compute the longest path.

### Advent of Code 2023, Day 23, Part 2

Link: https://adventofcode.com/2023/day/23

Given a map of trails, compute the longest path, ignoring the arrows and allowing
free travel, but not backtracking onto an already-visited path.

This greatly increased the number of combinations, but longest-path algorithms
still require brute force. This eventually finished, but could be sped up with
a better data structure that compresses the map into just intersecting nodes,
rather than traversing the paths every time.

### Advent of Code 2023, Day 24, Part 1

Link: https://adventofcode.com/2023/day/24

Given coordinates and velocities of "hailstones", consider just the X, Y
coordinates and calculate how many hailstones' paths will intersect within
a specific test area.

### Advent of Code 2023, Day 24, Part 2

Link: https://adventofcode.com/2023/day/24

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

### Advent of Code 2023, Day 25, Part 1

Link: https://adventofcode.com/2023/day/25

Given a set of "components" connected by wires, split them into two groups
based on cutting three wires, and figure out the number of components on
each side.

This is a graph problem of calculating clusters. However, this solution uses a
shortcut since we know there are exactly three paths connecting each cluster.
We take an arbitrary base node and for each other node, calculate the number
of unique minimal paths. A unique path is one that does not cross the same edge.

If the number of unique paths is equal to three, then we know the two nodes
are in opposite clusters, because we know the clusters are connected by exactly
three paths. If the count is more than three, then we know they're in the same
cluster.

The unique minimal path is calculated using Breadth-First-Search with a set to
keep track of edges already traveled.

The puzzle only wants the total number in each cluster, so this algorithm doesn't
try to identify the exact edges between the clusters. The edges could be identified
by tracking the common edges among pairs of nodes in opposite clusters.
