import json
from copy import deepcopy as copy
from constants import *


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
            if start_time < cstart_time < stop_time :
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

class Profile:
    def __init__(self, data):
        self.stroke_rate = get_stroke_rate(data)
        self.