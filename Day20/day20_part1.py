#!/usr/bin/python
"""Advent of Code 2023, Day 20, Part 1

https://adventofcode.com/2023/day/20

Simulates a set of "modules" wired together that send signals in a certain
connected structure. Based on the rules of each module, totals up the number
of "low pulses" and "high pulses" and multiples them.

See test.dat for sample data and modules.dat for full data.

Author: Tim Behrendsen
"""

import re
import sys
from queue import Queue

fn = 'test.dat'
fn = 'test2.dat'
fn = 'modules.dat'

modules = { }
total_low = 0
total_high = 0

#
# Base class for a module
#
class Module:
    def __init__(self, name):
        self.name = name
        self.connections = []

    # Add a connection to another module
    def add_connect(self, mod):
        self.connections.append(mod)

    def __repr__(self):
        s = f"[{self.name} ({self.get_type()}) "
        names = []
        for c in self.connections:
            names.append(c.name)

        s += ', '.join(names) + "]"
        return s

    def get_type(self):
        m = re.findall(r'__main__\.(\w+)', str(type(self)))
        return "UNK" if len(m) == 0 else m[0]

    # Send a pulse to all connected modules
    def send_all(self, pulse):
        global total_high, total_low

        new_ents = []
        for mod in self.connections:
            new_ents.append({ 'from': self, 'mod': mod, 'pulse': pulse })
            if pulse:
                total_high += 1
            else:
                total_low += 1

        return new_ents


#
# "FlipFlop" module
# High signals are ignored. If a low signal, flips state, and sends
# the state to the connect modules
#
class FlipFlop(Module):
    def __init__(self, name):
        super().__init__(name)
        self.state = 0

    # Recieve a pulse
    def rec_pulse(self, from_mod, pulse):
        # Ignore if high pulse 
        if pulse == 1:
            return []

        self.state = 1 - self.state
        return self.send_all(self.state)

#
# "Broadcaster" module. When button pressed, this is the first module.
# Sends pulse to all connected modules
#
class Broadcaster(Module):
    # Recieve a pulse
    def rec_pulse(self, from_mod, pulse):
        return self.send_all(pulse)

#
# "Conjunction" module. Rules
# When recieves a pulse from a remote module, stores that pulse.
# If all stored states are low, then it sends a high pulse to all
# connected modules.
#
class Conjunction(Module):
    def __init__(self, name):
        super().__init__(name)
        self.input_mods = { }

    # Add a module that will send signals to this one
    def add_input(self, mod):
        self.input_mods[mod.name] = { 'mod': mod, 'state': 0 }

    def __repr__(self):
        s = super().__repr__()
        names = []
        for c in self.input_mods.values():
            names.append(c['mod'].name)
        return s[0:-1] + " INP: " + ', '.join(names) + "]"

    # Recieve a pulse
    def rec_pulse(self, from_mod, pulse):
        self.input_mods[from_mod.name]['state'] = pulse

        # If any are low, it sends a high pulse
        pulse = 0

        for e in self.input_mods.values():
            if e['state'] == 0:
                pulse = 1
                break

        return self.send_all(pulse)

#
# Null module, used for module that didn't have a definition (used in Part 2)
#
class NullMod(Module):
    def rec_pulse(self, from_mod, pulse):
        return []

#
# "Output" module, used for debugging in the test data
#
class Output(Module):
    def rec_pulse(self, from_mod, pulse):
        print(f"    Output: Received {pulse}")
        return []

#
# "Click the button" which initiates signaling
#
def button():
    global total_low

    total_low += 1
    queue = Queue()
    queue.put({ 'from': None, 'mod': modules['broadcaster'], 'pulse': 0 })

    while not queue.empty():
        entry = queue.get()
        mod = entry['mod']
        new_ents = mod.rec_pulse(entry['from'], entry['pulse'])
        for e in new_ents:
            queue.put(e)

#
# Main processing.
#
def main():
    # Read in all the entries

    global modules

    module_data = []

    with open(fn, 'r') as file:
        for line in file:
            line = line.rstrip("\n")
            if line == '':
                break

            matches = re.findall(r'(.*) -> (.*)', line)
            name, con = matches[0]
            con_list = con.split(', ')

            c = name[0]
            if c == '%':
                mod = FlipFlop(name[1:])
            elif c == '&':
                mod = Conjunction(name[1:])
            elif name == 'broadcaster':
                mod = Broadcaster(name)
            else:
                print("BAD TYPE {name}")
                exit(0)

            modules[mod.name] = mod
            module_data.append({ 'mod': mod, 'list': con_list })

    # Create special debug output module
    modules['output'] = Output('output')

    for d in module_data:
        mod = d['mod']
        for con_name in d['list']:
            con_mod = modules.get(con_name, None)
            if con_mod == None:
                con_mod = NullMod(con_name)

            mod.add_connect(con_mod)

            # Conjunctions need to track input modules
            if isinstance(con_mod, Conjunction):
                con_mod.add_input(mod)

    # Count 1000 button presses
    for i in range(1000):
        count = button()

    #print(f"total_low = {total_low}, total_high = {total_high}")

    return total_low * total_high

pulse_count = main()
print(f"Pulse product is {pulse_count}")
