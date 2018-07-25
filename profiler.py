import json
import sys

from copy import deepcopy as copy
from constants import *
from parser import *


# Searches two lists of KeyPress objects to try to find matching 
# sequences of key-presses. E.g. Two users type the word "cat".
# Currently too slow for large data sets
def get_keypress_intersects(key_presses1, key_presses2, min_intersect_len=2):
    len1 = len(key_presses1)
    len2 = len(key_presses2)
    counter = 0
    intersects = []
    for start1 in range(len1 - 1):
        for start2 in range(len2 - 1):
            if key_presses1[start1] == key_presses2[start2]:
                next1 = start1 + 1
                next2 = start2 + 1
                while ((next1 < len1 and next2 < len2) and
                        key_presses1[next1] == key_presses2[next2]):
                    slice1 = slice(start1, next1, 1)
                    slice2 = slice(start2, next2, 1)
                    key_slice1 = key_presses1[slice1]
                    key_slice2 = key_presses2[slice2]
                    intersects.append((key_slice1, key_slice2))
                    next1 += 1
                    next2 += 1
                    counter += 1
    print(counter)
    return intersects


# Finds the amount of overlap between two lists of KeyPress objects
# These lists should likely be standardized (see standardize function)
def intersect_area(key_presses1, key_presses2):
    assert len(key_presses1) == len(key_presses2)
    area = 0
    for kpi in range(len(key_presses1)):
        kp1 = key_presses1[kpi]
        kp2 = key_presses2[kpi]
        max_min = max(kp1.start_time, kp2.start_time)
        min_max = min(kp1.stop_time, kp2.stop_time)
        if max_min >= min_max:
            continue
        x_intersect = min_max - max_min
        area += x_intersect
    return area


# Shift times for sequence of KeyPress objects by amount.
# This is often used to compare two sequences and is performed.
# Should usually be performed before the stretch function
def shift(key_presses, amount):
    outs = []
    for kp in key_presses:
        _min = kp.start_time
        _max = kp.stop_time
        new_min = _min + amount
        new_max = _max + amount
        kp_copy = copy(kp)
        kp_copy.start_time = new_min
        kp_copy.stop_time = new_max
        outs.append(kp_copy)
    return outs


# Stretch the times for sequence of KeyPress objects by factor.
# Use of this is optional for standardization
def stretch(key_presses, factor):
    outs = []
    for kp in key_presses:
        _min = kp.start_time
        _max = kp.stop_time
        new_min = _min * factor
        new_max = _max * factor
        kp_copy = copy(kp)
        kp_copy.start_time = new_min
        kp_copy.stop_time = new_max
        outs.append(kp_copy)
    return outs


# Standardize a sequence of KeyPress events so that the KeyPress event
# beginning at time=0. If do_stretch is set to True, the total time from
# start to finish will be the value of standard_span.
def standardize(key_presses, do_stretch=False, standard_span=1000):
    min_time = key_presses[0].start_time
    max_time = key_presses[0].stop_time
    for kp in key_presses:
        if kp.start_time < min_time:
            min_time = kp.start_time
        if kp.stop_time > max_time:
            max_time = kp.stop_time
    left_shift = min_time
    span = max_time - min_time
    shrink_factor = float(span) / standard_span
    out_key_presses = shift(key_presses, -left_shift)
    stretch_factor = 1.0/shrink_factor
    if do_stretch:
        return stretch(out_key_presses, stretch_factor)
    else:
        return out_key_presses


# Align KeyPress event times such that the overlap to the left is
# equal to the overlap of the right (I think. I forgot exactly where
# t_shift comes from)
def auto_align_key_pressess(key_presses1, key_presses2):
    s = copy(key_presses1)
    t = copy(key_presses2)
    t_shift = 0
    for i in range(len(key_presses1)):
            t_shift += ((s[i].start_time + s[i].stop_time) -
                        (t[i].start_time + t[i].stop_time))
    t_shift = t_shift / (2*len(key_presses1))
    shifted_t = shift(t, t_shift)
    return s, shifted_t


# Find the average intersection area of each KeyPress event
def get_average_area(intersects):
    total_areas = 0
    total_rows = 0
    for tup in intersects:
            key_presses1, key_presses2 = tup
            # total_rows += len(key_presses1)
            # Above puts less weight on longer matching sequences.
            total_rows += 1
            s1, s2 = map(standardize, (key_presses1, key_presses2))
            key_presses1, key_presses2 = auto_align_key_pressess(s1, s2)
            area = intersect_area(key_presses1, key_presses2)
            total_areas += area
    average = float(total_areas) / total_rows
    return average


# basic test to see if the author of the third file is the same
# as the first or second file
def compare(dataset1, dataset2, dataset3):
    kp1, kp2, kp3 = map(get_simple_key_presses, (dataset1, dataset2, dataset3))
    akp1, akp2, akp3 = map(get_complex_key_presses, (kp1, kp2, kp3))
    intersects1 = get_keypress_intersects(akp1, akp3)
    intersects2 = get_keypress_intersects(akp2, akp3)
    average1 = get_average_area(intersects1)
    average2 = get_average_area(intersects2)
    a1 = sys.argv[1]
    a2 = sys.argv[2]
    a3 = sys.argv[3]
    print(AUTHOR_TEMPLATE.format(a3, a1 if average1 > average2 else a2))


def run():
    if len(sys.argv) < 2:
        print BASIC_CONSOLE_TEMPLATE.format(sys.argv[0])
        exit(1)

    command = sys.argv[1]
    if command == "compare":
        with open(sys.argv[2]) as fp:
            dataset1 = json.load(fp)
        with open(sys.argv[3]) as fp:
            dataset2 = json.load(fp)
        with open(sys.argv[4]) as fp:
            dataset3 = json.load(fp)
        compare(dataset1, dataset2, dataset3)
        # exit(0)
    elif command == "visualize":
        with open(sys.argv[2]) as fp:
            dataset = json.load(fp)
            kps = get_simple_key_presses(dataset)
            visualize(kps)
            exit(0)
    else:
        print BASIC_CONSOLE_TEMPLATE.format(sys.argv[0])
        exit(1)


if __name__ == '__main__':
    import timeit
    print(timeit.repeat("run()", setup="from __main__ import run", number=1))
    #run()

