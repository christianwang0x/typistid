import json
from copy import deepcopy as copy
from constants import *
import sys

raw_data=[[0, 67, 0],
          [1000, 65, 0],
          [2000, 82, 0],
          [3000, 67, 1],
          [4000, 66, 0],
          [5000, 66, 1],
          [6000, 82, 1],
          [7000, 79, 0],
          [8000, 65, 1],
          [9000, 78, 0],
          [10000, 79, 1],
          [11000, 78, 1]]


class KeyPress:
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

    def __repr__(self):
        output = KEYPRESS_TEMPLATE.format(code=self.code,
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


    def __eq__(self, other):
        if self.code == other.code:
            return True


def get_simple_key_presses(data):
    key_presses = []
    for index in range(len(data)):
        event = data[index]
        if event[D] == DOWN:
            kp = KeyPress(data)
            kp.code = event[K]
            kp.start_index = index
            kp.start_time = event[T]
            for cindex in range(index + 1, len(data)):
                cevent = data[cindex]
                if cevent[K] == event[K] and cevent[D] == UP:
                    kp.stop_index = cindex
                    kp.stop_time = cevent[T]
                    break
            key_presses.append(kp)
    return key_presses


def get_complex_key_presses(data):
    key_presses = get_simple_key_presses(data)
    for index in range(len(key_presses)):
        kp = key_presses[index]
        start_time = kp.start_time
        stop_time = kp.stop_time
        for cindex in range(index+1, len(key_presses)):
            ckp = key_presses[cindex]
            cstart_time = ckp.start_time
            cstop_time = ckp.stop_time
            if start_time < cstart_time < stop_time:
                if cstop_time < stop_time:
                    ckp.parents.append(kp)
                    kp.children.append(ckp)
                else:
                    ckp.step_parents.append(kp)
                    kp.step_children.append(ckp)
            elif cstart_time < start_time < cstop_time:
                if stop_time < cstop_time:
                    kp.parents.append(ckp)
                    ckp.children.append(kp)
                else:
                    kp.step_parents.append(ckp)
                    ckp.step_children.append(kp)
    return key_presses


def get_key_downs(data):
    return get_keys_of_type(data, DOWN)


def get_key_ups(data):
    return get_keys_of_type(data, UP)


def get_keys_of_type(data, direction):
    out_data = []
    for (t, k, d) in data:
        if d == direction:
            out_data.append([t, k, d])
    return out_data


def get_stroke_rate(data):
    start_time = data[0][0]
    stop_time = data[-1][0]
    delta_time = stop_time - start_time
    downs = get_key_downs(data)
    rate = len(downs) / TIME_UNITS / delta_time
    return rate


def contains(small, big):
    for i in xrange(len(big)-len(small)+1):
        for j in xrange(len(small)):
            if big[i+j] != small[j]:
                break
        else:
            return i, i+len(small)
    return False


def get_slices(min_slice_len, max_slice_len, max_index):
    slices = []
    for slice_len in range(min_slice_len, max_slice_len+1):
        for index in range(max_index+1 - slice_len):
            slices.append(slice(index, index + slice_len, 1))
    return slices


def get_keypress_intersects(key_presses1, key_presses2, min_intersect_len=2):
    intersects = []
    smaller_kp, larger_kp = sorted([key_presses1, key_presses2], key=len)
    min_slices = get_slices(min_intersect_len, len(smaller_kp), len(smaller_kp))
    max_slices = get_slices(min_intersect_len, len(smaller_kp), len(larger_kp))
    for min_slice in min_slices:
        for max_slice in max_slices:
            slice1 = smaller_kp[min_slice]
            slice2 = larger_kp[max_slice]
            if slice1 == slice2:
                for kp in slice1:
                    if kp.code == 32:
                        break
                else:
                    intersects.append((slice1, slice2))
    return intersects


def intersect_area(sample1, sample2):
    assert len(sample1) == len(sample2)
    area = 0
    for kpi in range(len(sample1)):
        kp1 = sample1[kpi]
        kp2 = sample2[kpi]
        r1 = (kp1.start_time, kp1.stop_time)
        r2 = (kp2.start_time, kp2.stop_time)
        maxmin = max(r1[0], r2[0])
        minmax = min(r1[1], r2[1])
        if maxmin >= minmax:
            continue
        x_intersect = minmax - maxmin
        area += x_intersect
    return area


def shift(sample, amount):
    outs = []
    for kp in sample:
        _min = kp.start_time
        _max = kp.stop_time
        newmin = _min + amount
        newmax = _max + amount
        kp_copy = copy(kp)
        kp_copy.start_time = newmin
        kp_copy.stop_time = newmax
        outs.append(kp_copy)
    return outs


def stretch(sample, factor):
    outs = []
    for kp in sample:
        _min = kp.start_time
        _max = kp.stop_time
        newmin = _min * factor
        newmax = _max * factor
        kp_copy = copy(kp)
        kp_copy.start_time = newmin
        kp_copy.stop_time = newmax
        outs.append(kp_copy)
    return outs


def standardize(sample, standard_span=1000):
    mintime = sample[0].start_time
    maxtime = sample[0].stop_time
    for kp in sample:
        if kp.start_time < mintime:
            mintime = kp.start_time
        if kp.stop_time > maxtime:
            maxtime = kp.stop_time
    left_shift = mintime
    span = maxtime - mintime
    shrink_factor = float(span) / standard_span
    out_sample = shift(sample, -left_shift)
    stretch_factor = 1.0/shrink_factor
    return stretch(out_sample, stretch_factor)


def auto_align_samples(sample1, sample2):
    s = copy(sample1)
    t = copy(sample2)
    t_shift = 0
    for i in range(len(sample1)):
            t_shift += (s[i].start_time + s[i].stop_time) - (t[i].start_time + t[i].stop_time)
    t_shift = t_shift / (2*len(sample1))
    shifted_t = shift(t, t_shift)
    return s, shifted_t


def get_average_area(intersects):
    total_areas = 0
    total_rows = 0
    for tup in intersects:
            sample1, sample2 = tup
            total_rows += len(sample1)
            s1, s2 = map(standardize, (sample1, sample2))
            sample1, sample2 = auto_align_samples(s1, s2)
            area = intersect_area(sample1, sample2)
            total_areas += area
    average = float(total_areas) / total_rows
    return average

def test():
    max_keystrokes = None
    if len(sys.argv) > 1:
        max_keystrokes = int(sys.argv[1])
    with open('resources/sample1.json') as fp:
        dataset1 = json.load(fp)[:max_keystrokes]
    with open('resources/sample2.json') as fp:
        dataset2 = json.load(fp)[:max_keystrokes]
    with open('resources/sample3.json') as fp:
        dataset3 = json.load(fp)[:max_keystrokes]
    kp1 = get_complex_key_presses(dataset1)
    kp2 = get_complex_key_presses(dataset2)
    kp3 = get_complex_key_presses(dataset3)
    intersects1 = get_keypress_intersects(kp1, kp3)
    intersects2 = get_keypress_intersects(kp2, kp3)
    average1 = get_average_area(intersects1)
    average2 = get_average_area(intersects2)
    print("Test author is same as author of sample {0}.".format(1 if average1 > average2 else 2))

test()

