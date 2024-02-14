#!/usr/bin/python
"""Advent of Code 2023, Day 20, Part 2

https://adventofcode.com/2023/day/20

Simulates a set of "modules" wired together that send signals in a certain
connected structure. For part 2, need to track the signal to 'rx' and predict
the fewest number of button presses required to recieve a low pulse.

This required looking back at the four "Conjunction" modules connected to 'rx'
and noticing that they have a repeating pattern. The repeating patterns turned
out to be four prime numbers, and it will only send the low pulse when each
of those triggered. So the code figures out the cycle times for each of
the four modules, and the product of the primes is the answer.

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
button_count = 0

# Flag so we only count 'rx' cycle once per button
first_rx = False

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
        new_ents = []
        for mod in self.connections:
            new_ents.append({ 'from': self, 'mod': mod, 'pulse': pulse })

        return new_ents

#
# "Flip Flop" module
# High signals are ignored. If a low signal, flips state, and sends
# the state to the connect modules
#
class FlipFlop(Module):
    def __init__(self, name):
        super().__init__(name)
        self.state = 0

    # Recieve a pule
    def rec_pulse(self, from_mod, pulse):
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
# Read back from module and gather connected conjunction nodes
#
def get_conj_tree(mod, level):
    indent = ' ' * (level*4+4)
    vals = []

    for c in mod.input_mods.values():
        sub_mod = c['mod']
        s = sub_mod.name
        #print(f"{indent}{sub_mod.name}:{c['state']}")
        vals.append(c['state'])
        if isinstance(sub_mod, Conjunction):
            sub_vals = get_conj_tree(sub_mod, level+1)
            vals.append(sub_vals)

    return vals

#
# Track the cycles of the conjunction modules
#
last_pulse = [ 0, 0, 0, 0]
diffs = [ 0, 0, 0, 0]
last_diffs = [ 0, 0, 0, 0 ]
diffs_count = 0

def calc_cycles(mod):
    # Gather the conjunction node values up the tree from rx
    # Looks like:
    #[0, [1, [1, 0, 0, 0, 0, 1, 1, 1, 1]], 0, [1, [0, 1, 1, 0, 1, 1, 0]], 0, [1, [0, 1, 0, 0, 0, 1, 0, 1, 1]], 0, [1, [0, 1, 1, 0, 0, 1, 1]]]
    vals = get_conj_tree(mod, 0)

    global diffs, last_diffs, diffs_count

    chk = [ vals[0], vals[2], vals[4], vals[6] ]
    for i in range(4):
        n = chk[i]    
        if n != 0:
            if last_pulse[i] != 0:
                diffs[i] = button_count - last_pulse[i]
            last_pulse[i] = button_count

    if diffs[0] != 0 and diffs[1] != 0 and diffs[2] != 0 and diffs[3] != 0:
        if last_diffs[0] == 0:
            last_diffs = diffs
        else:
            if diffs == last_diffs:
                diffs_count += 1
                # Make sure doesn't change for 10 cycles
                if diffs_count > 10:
                    min_cycle = diffs[0] * diffs[1] * diffs[2] * diffs[3]
                    print(f"ANSWER IS: {min_cycle}")
                    exit(0)
            else:
                last_diffs = diffs.copy()
                diffs_count = 0

    return

#
# Special ending module attached to 'rx' to recieve the final signal.
# This is where we detect the pattern.
#
# This gets called multiple times on each press of the button, so we
# use the 'first_rx' flag to only count on the first time after a button
# press.
#
class EndingMod(Module):
    def rec_pulse(self, from_mod, pulse):
        global first_rx

        if first_rx:
            calc_cycles(from_mod)
        first_rx = False

        # This can't really happen in anyone's lifetime
        if pulse == 0:
            print(f"ENDING MOD, pulse = {pulse}, count = {button_count}")
            exit(0)

        return []

#
# Null module, used for module that didn't have a definition (not used in Part 2)
#
class NullMod(Module):
    def rec_pulse(self, from_mod, pulse):
        return []

#
# "Output" module, used for debugging in the test data
#
class Output(Module):
    def rec_pulse(self, from_mod, pulse):
        return []

#
# "Click the button" which initiates signaling
#
def button():
    global button_count
    global first_rx
    first_rx = True

    button_count += 1

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

    # Special ending mod
    modules['rx'] = EndingMod('rx')

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

    # Continue processing until the cycle is detected
    while True:
        button()

    return

main()
