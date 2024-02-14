#!/usr/bin/python
"""Advent of Code 2023, Day 19, Part 1

https://adventofcode.com/2023/day/19

Given a set of rules, process them for each "part" description, totaling
the "rating number" for the accepted parts.

See test.dat for sample data and rules.dat for full data.

Author: Tim Behrendsen
"""

import re
import sys

fn = 'test.dat'
fn = 'rules.dat'

#
# A "part", which has four attribute values (x, m, a, s)
#
class Part:
    def __init__(self, line):
        matches = re.findall(r'\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}', line)
        self.x, self.m, self.a, self.s = [ int(n) for n in matches[0] ]
        pass

    def __repr__(self):
        return f"[x={self.x},m={self.m},a={self.a},s={self.s}]"

    def get_num(self, nm):
        return getattr(self, nm)

    # "Part rating" is total of the attribute numbers
    def get_rating(self):
        return self.x + self.m + self.a + self.s

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
# Main processing.
#
def main():
    # Read in all the entries

    workflows = { }
    part_list = []

    with open(fn, 'r') as file:
        # First read workflows
        while True:
            line = file.readline()
            if line == '\n':
                break

            workflow = Workflow(line)
            workflows[workflow.get_name()] = workflow

        # Next read parts
        while True:
            line = file.readline()
            if line == '':
                break

            part = Part(line)
            part_list.append(part)

    # Process each part, determining if it's accepted by the rules.
    # If so, total up the "part rating"
    total = 0
    for part in part_list:
        cur_flow = 'in'
        result = ''
        while cur_flow != None:
            workflow = workflows[cur_flow]
            for rule in workflow.rules:
                # A = accept part, R = Reject part
                if rule.op in ('A', 'R'):
                    result = rule.op
                    cur_flow = None
                    break

                # NEXT = Move to to next workflow
                elif rule.op == 'NEXT':
                    cur_flow = rule.next_rule
                    break

                # Compare attribute less than number
                elif rule.op == '<':
                    n = part.get_num(rule.attr)
                    if n < rule.value:
                        if rule.next_rule in ('A', 'R'):
                            result = rule.next_rule
                            cur_flow = None
                            break
                        else:
                            cur_flow = rule.next_rule
                            break

                # Compare attribute greater than number
                elif rule.op == '>':
                    n = part.get_num(rule.attr)
                    if n > rule.value:
                        if rule.next_rule in ('A', 'R'):
                            result = rule.next_rule
                            cur_flow = None
                            break
                        else:
                            cur_flow = rule.next_rule
                            break
                        
        if result == 'A':
            total += part.get_rating()

    return total

total = main()
print(f"Total ratings is {total}")
