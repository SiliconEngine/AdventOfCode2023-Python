#!/usr/bin/python
"""Advent of Code 2023, Day 19, Part 2

https://adventofcode.com/2023/day/19

Given a set of rules that will produce either "Accept" or "Reject" for a part
based on its attributes, calculate the total number of combinations of part
numbers that will be accepted.

In part 1, we processed the rule for a specific part. This processes the
rules for a range of values, recursively checking different paths based on
the rules, and then totals of the combinations.

See test.dat for sample data and rules.dat for full data.

Author: Tim Behrendsen
"""

import re
import sys

fn = 'test.dat'
fn = 'rules.dat'

workflows = { }

#
# A rule part of a work flow.
#
class Rule:
    def __init__(self, op, next_rule = None, attr = None, value = None):
        if value != None:
            value = int(value)
        self.op, self.attr, self.value, self.next_rule = op, attr, value, next_rule

    def __repr__(self):
        if self.op == 'NEXT':
            return f"[{self.op} {self.next_rule}]"
        if self.op in ('A', 'R'):
            return f"[{self.op}]"

        return f"[{self.op} {self.attr}, {self.value}, {self.next_rule}]"

#
# Class to represent a "workflow", which is a set of rules
#
class Workflow:
    def __init__(self, line):
        matches = re.findall(r'(\w+)\{(.*)\}', line)
        self.name = matches[0][0]
        rules_s = matches[0][1]
        self.rules = []

        for r_s in rules_s.split(','):
            # Check for [A]ccept or [R]eject
            if r_s == 'R' or r_s == 'A':
                rule = Rule(r_s)
                self.rules.append(rule)
                continue

            # Check for rule like: s<1351:px
            matches = re.findall(r'(.)(\<|\>)(\d+):(\w+)', r_s)
            if len(matches) > 0:
                attr, op, value, next_rule = matches[0]
                rule = Rule(op, next_rule, attr, int(value))
                self.rules.append(rule)
                continue

            # Must be redirect to next rule
            rule = Rule('NEXT', r_s)
            self.rules.append(rule)

    def __repr__(self):
        return f"Workflow {self.name}: {self.rules}"

    def get_name(self):
        return self.name

#
# Calculate total combinations of a range of (x,m,a,s) attributes
#
def get_total(rating_ranges):
    total = 1
    for r in rating_ranges.values():
        total *= r[1] - r[0] + 1
    return total

#
# Recursive routine to process single flow of rules, potentially
# branching if we need to.
#
def recurse_rule(flow, rule_num, rating_ranges, level):
    indent = ' ' * (level*4)

    while True:
        rule = flow.rules[rule_num]
        rule_num += 1

        # Reject, no valid combos
        if rule.op == 'R':
            return 0

        # Accept, return combo count
        elif rule.op == 'A':
            total = get_total(rating_ranges)
            return total

        # Next workflow, just do move
        elif rule.op == 'NEXT':
            flow = workflows[rule.next_rule]
            rule_num = 0
            continue

        elif rule.op == '<':
            # Compare range less than number, potentially doing recursive call
            # if we have multiple paths
            attr = rule.attr
            rg = rating_ranges[attr]
            n = rule.value
            # Three possibilities: Above both, below both, between
            # CHECK: (1, 4000)    < 1351   : Recurse to match (1, 1350) : no-match (1351, 4000)
            # CHECK: (2000, 4000) < 1351   : Rule always doesn't match, process no-match
            # CHECK: (1000, 1010) < 1351   : Rule always matches
            # CHECK: (1351, 4000) < 1351   : Rule always doesn't match (edge case), process no-match
            # CHECK: (1, 1351)    < 1351   : Recurse (edge case)

            if n > rg[1]:
                # Always matches, process move
                if rule.next_rule == 'R':
                    # Reject, no combos
                    return 0
                elif rule.next_rule == 'A':
                    # Accept, calculate combos to total
                    return get_total(rr_copy)
                else:
                    # Move to new work flow, just continue
                    rule_num = 0
                    flow = workflows[rule.next_rule]

            elif n <= rg[0]:
                # Always no-match, go to next rule_num
                rating_ranges[attr] = (0, -1)

            elif n > rg[0] and n <= rg[1]:
                # Need to recurse two paths
                total = 0
                rr_copy = rating_ranges.copy()

                # PATH 1: does not match rule, go to next rule
                rr_copy[attr] = (n, rg[1])
                total += recurse_rule(flow, rule_num, rr_copy, level+1)

                # PATH 2: Matches rule, use jump
                rr_copy[attr] = (rg[0], n-1)
                if rule.next_rule == 'R':
                    pass
                elif rule.next_rule == 'A':
                    total += get_total(rr_copy)
                else:
                    total += recurse_rule(workflows[rule.next_rule], 0, rr_copy, level+1)

                return total

        elif rule.op == '>':
            # Compare range greater than number, potentially doing recursive call
            # if we have multiple paths
            attr = rule.attr
            rg = rating_ranges[attr]
            n = rule.value
            # Three possibilities: Above both, below both, between
            # CHECK: (1, 4000)    > 1351   : Recurse to match (1352, 4000) : no-match (1, 1351)
            # CHECK: (2000, 4000) > 1351   : Rule always matches
            # CHECK: (1000, 1010) > 1351   : Rule always doesn't match
            # CHECK: (1351, 4000) > 1351   : Recurse (edge case)
            # CHECK: (1, 1351)    > 1351   : Rule always doesn't match (edge case), process no-match

            if rg[0] > n:
                # Always matches, process move
                if rule.next_rule == 'R':
                    # Reject, no combos
                    return 0
                elif rule.next_rule == 'A':
                    # Accept, calculate combos to total
                    return get_total(rr_copy)
                else:
                    # Move to new work flow, just continue
                    rule_num = 0
                    flow = workflows[rule.next_rule]

            elif n > rg[1]:
                # Always no-match, go to next rule_num
                rating_ranges[attr] = (0, -1)

            elif n >= rg[0] and n < rg[1]:
                # Need to recurse two paths
                total = 0
                rr_copy = rating_ranges.copy()

                # PATH 1: does not match rule, go to next rule
                rr_copy[attr] = (rg[0], n)
                total += recurse_rule(flow, rule_num, rr_copy, level+1)

                # PATH 2: Matches rule, use jump
                rr_copy[attr] = (n+1, rg[1])
                if rule.next_rule == 'R':
                    pass
                elif rule.next_rule == 'A':
                    total += get_total(rr_copy)
                else:
                    total += recurse_rule(workflows[rule.next_rule], 0, rr_copy, level+1)

                return total

    raise Exception("Should not hit here")

#
# Calculate number of combinations for the puzzle range.
#
def calc_combos():
    cur_flow = 'in'
    rating_ranges = {'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000)}
    flow = workflows['in']

    total = recurse_rule(flow, 0, rating_ranges, 0)
    return total

#
# Main processing.
#
def main():
    # Read in all the entries

    global workflows

    with open(fn, 'r') as file:
        # First read workflows
        while True:
            line = file.readline()
            if line == '\n':
                break

            workflow = Workflow(line)
            workflows[workflow.get_name()] = workflow

        # Rest is parts, which is no longer needed
        pass

    total = calc_combos()
    return total

total = main()
print(f"Total valid combinations is {total}")
