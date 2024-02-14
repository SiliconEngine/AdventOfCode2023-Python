#!/usr/bin/python
"""Advent of Code 2023, Day 25, Part 1

https://adventofcode.com/2023/day/25

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

See test.dat for sample data and diagram.dat for full data.

Author: Tim Behrendsen
"""

# Set to True to generate a visualization of the graph
visualize = False

import re
import sys

if visualize:
    import networkx as nx
    import matplotlib.pyplot as plt

fn = 'test.dat'
fn = 'diagram.dat'

def make_edge(n1, n2):
    if n1 < n2:
        return f"{n1}-{n2}"
    else:
        return f"{n2}-{n1}"

class Component:
    def __init__(self, name):
        self.name = name
        self.wires = [ ]

    def __repr__(self):
        return f"[{self.name}: {', '.join(w.name for w in self.wires)}]"

    def set_link(self, rmt):
        if rmt not in self.wires:
            self.wires.append(rmt)

class ComponentSet:
    def __init__(self):
        self.comps = { }

    def add_comp(self, name, wire_list):
        comp = self.comps.get(name)
        if comp == None:
            comp = self.comps[name] = Component(name)

        for rmt_name in wire_list:
            rmt = self.comps.get(rmt_name)
            if rmt == None:
                rmt = self.comps[rmt_name] = Component(rmt_name)

            comp.set_link(rmt)
            rmt.set_link(comp)

    def dump(self):
        for name in self.comps:
            print(self.comps[name])

    def visualize(self):
        G = nx.Graph()
        for name, comp in self.comps.items():
            G.add_node(name)
            for rmt in comp.wires:
                G.add_edge(name, rmt.name)
        plt.figure(figsize=(10, 8))
        nx.draw(G, with_labels=True, node_color='skyblue', node_size=700, edge_color='k', linewidths=1, font_size=15, )
        plt.show()

    #
    # Find a single path that hasn't traveled a prior used edge
    #
    def find_path(self, edge_chk_set, comp, target_name):
        node_chk_set = set()
        node_chk_set.add(comp.name)

        # Node for BFS
        class QNode:
            def __init__(self, path, comp):
                self.path = path
                self.comp = comp

        q = [ QNode([comp.name] , comp) ]

        # Get next node on the BFS queue
        while q:
            node = q.pop()
            path = node.path
            comp = node.comp

            # Follow each wire and see if we've scanned this edge before
            for rmt in comp.wires:
                edge = make_edge(comp.name, rmt.name)

                # If we've already visited this node in this run, skip
                if rmt.name in node_chk_set:
                    continue

                # If we've already used this edge in a path, skip
                if edge in edge_chk_set:
                    continue
                edge_chk_set.add(edge)

                # If found ending node, stop
                if rmt.name == target_name:
                    path.append(target_name)
                    return path

                # Add this new node to the queue
                node_chk_set.add(rmt.name)
                new_path = path.copy()
                new_path.append(rmt.name)
                q.append(QNode(new_path, rmt))

        # No further paths found
        return []

    #
    # Count how many minimal paths to travel from comp1 to comp2
    # Uses breadth-first-search (BFS) algorithm
    #
    def count_paths(self, comp1, comp2):
        cur_edge_chk_set = set()            # Edges checked, tracked across runs
        target_name = comp2.name

        # Continue checking for paths until no further available
        count = 0
        while True:
            # Find a single path that doesn't follow a prior edge
            edge_chk_set = cur_edge_chk_set.copy()
            path = self.find_path(edge_chk_set, comp1, target_name)

            # If no more paths, stop
            if not path:
                break

            # Found a new path, add the edges to the already-traveled list
            count += 1
            last = comp1.name
            for p in path:
                edge = make_edge(last, p)
                cur_edge_chk_set.add(edge)
                last = p

        return count

    #
    # Figure out how many nodes are within the two clusters
    #
    def scan_paths(self):
        comp_list = list(self.comps.values())

        # Start with a base node and compare to the rest
        base_node = comp_list[0]
        count1 = 0
        count2 = 0
        for idx in range(1, len(comp_list)):
            comp = comp_list[idx]
            count = self.count_paths(base_node, comp)
            print(f"{base_node.name} to {comp.name}: count = {count}")

            # If number of paths is more than three, then we know this node
            # is part of the same cluster as the base node.
            if count > 3:
                count2 += 1
            else:
                count1 += 1

        # Add one more for the base node
        count2 += 1
        print(f"side1 = {count1}, side2 = {count2}, prod = {count1 * count2}")
        return count1 * count2

#
# Main processing.
#
def main():
    # Read in all the components
    comps = ComponentSet()

    with open(fn, 'r') as file:
        for line in file:
            line = line.rstrip('\n')
            matches = re.findall(r'(\b\w+\b)', line)
            name = matches[0]
            wire_list = matches[1:]
            comps.add_comp(name, wire_list)

    #comps.dump()
    answer = comps.scan_paths()

    if visualize:
        comps.visualize()

    return answer

answer = main()
print(f"Answer is {answer}")
