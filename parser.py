from constants import *
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

# Represents a full keypress event, from KEY_DOWN to KEY_UP and
# all related keypress events (parents, children, etc.)
class KeyPress:

    # Initialize instance attributes.
    # Data should not be duplicated because it should be a list-like
    # object. Otherwise large memory areas may be used as many KeyPress
    # objects are instantiated.
    def __init__(self, data):
        self.data = data
        self.code = None
        self.start_index = None
        self.stop_index = None
        self.start_time = None
        self.stop_time = None
        self.children = []
        self.step_children = []
        self.parents = []
        self.step_parents = []

    # Returns instance attributes in human-readable format.
    # Instead of child/parent lists this returns their lengths
    # as otherwise would return very large/infinite output.
    def __repr__(self):
        kt = KEYPRESS_TEMPLATE
        output = kt.format(code=self.code,
                           key=IKEYS[self.code],
                           start_index=self.start_index,
                           stop_index=self.stop_index,
                           start_time=self.start_time,
                           stop_time=self.stop_time,
                           children=len(self.children),
                           step_children=len(self.step_children),
                           parents=len(self.parents),
                           step_parents=len(self.step_parents))
        return output

    # Instances are considered equal if the key code is the same.
    # Time/relationships don't matter. This is for easy comparisons between two
    # arrays of key-presses.
    # E.g. Two different users type the word "cat"
    def __eq__(self, other):
        if self.code == other.code:
            return True


# Return raw event data for KEY_UPs or KEY_DOWNs.
def get_keys_of_type(data, direction):
    out_data = []
    for (t, k, d) in data:
        if d == direction:
            out_data.append([t, k, d])
    return out_data


# Get average keystroke rate in keystrokes per second.
# The divisor TIME_UNITS is the number seconds per time
# unit in the raw data.
def get_stroke_rate(data):
    start_time = data[0][0]
    stop_time = data[-1][0]
    delta_time = stop_time - start_time
    downs = get_keys_of_type(data, DOWN)
    rate = len(downs) / TIME_UNITS / delta_time
    return rate


# Convert raw JSON data to KeyPress instances with time
# attributes.
def get_simple_key_presses(raw_data):
    key_presses = []
    for index in range(len(raw_data)):
        event = raw_data[index]
        if event[D] == DOWN:
            kp = KeyPress(raw_data)
            kp.code = event[K]
            kp.start_index = index
            kp.start_time = event[T]
            for cindex in range(index + 1, len(raw_data)):
                cevent = raw_data[cindex]
                if cevent[K] == event[K] and cevent[D] == UP:
                    kp.stop_index = cindex
                    kp.stop_time = cevent[T]
                    break
            key_presses.append(kp)
    return key_presses


# Add advanced attributes to KeyPress list
# like parent-child relationships
def get_complex_key_presses(key_presses):
    for index in range(len(key_presses)):
        kp = key_presses[index]
        for cindex in range(index+1, len(key_presses)):
            ckp = key_presses[cindex]
            for parent, child in [(kp, ckp), (ckp, kp)]:
                if parent.start_time < child.start_time < parent.stop_time:
                    if child.stop_time < parent.stop_time:
                        child.parents.append(parent)
                        parent.children.append(child)
                    else:
                        child.step_parents.append(parent)
                        parent.step_children.append(child)
    return key_presses


# generate a graph for a list of KeyPresses
def visualize(key_presses):
    kps = deepcopy([kp for kp in key_presses if kp.start_time and kp.stop_time])
    start_list = [kp.start_time for kp in kps]
    stop_list = [kp.stop_time for kp in kps]
    yval = [IKEYS[kp.code] for kp in kps]
    start = np.asarray(start_list)
    stop = np.asarray(stop_list)
    width = stop - start
    fig, ax = plt.subplots()
    ax.barh(y=np.arange(len(yval)), width=width, left=start, height=0.9)
    ax.set_yticks(np.arange(len(yval)))
    ax.set_yticklabels(yval)
    ax.invert_yaxis()
    plt.xlabel("Time since page opened (ms)")
    plt.ylabel("Key pressed")
    plt.title("Key Press - Time Visualization")
    plt.show()
