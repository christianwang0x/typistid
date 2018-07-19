import json
from copy import deepcopy as copy
from constants import *


raw_data=[[9934,16,0],
          [10553,67,0],
          [10687,67,1],
          [10716,16,1],
          [10958,82,0],
          [11053,82,1],
          [11142,79,0],
          [11248,79,1],
          [11312,87,0],
          [11403,87,1]]


class KeyPress:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop
        self.children = []
        self.step_children = []


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

def get_shifted_keys(data):
    shift_list = []
    current_shift = []
    inshift = False
    for (t, k, d) in data:
        if k == KEYS["shift"]:
            if d == DOWN:
                current_shift = [[t, k, d]]
                inshift = True
            elif d == UP:
                current_shift.append([t, k, d])
                shift_list.append(copy(current_shift))
                current_shift = []
                inshift = False
        else:
            if inshift:
                current_shift.append([t, k, d])
    return shift_list

def get_shifted_keys_by_type(shift_event, event_type="all"):
    current_down_keys = []
    fully_enclosed_keys = []
    left_overlap_keys = []
    shift_enclosed = shift_event[1:-1]
    for event in shift_enclosed:
        if event[D] == DOWN:
            current_down_keys.append(event)
        elif event[D] == UP:
            for current_event in current_down_keys:
                if event[K] == current_event[K]:
                    current_down_keys.remove(current_event)
                    fully_enclosed_keys.append(current_event)
                    fully_enclosed_keys.append(event)
                    break
            else:
                left_overlap_keys.append(event)
    right_overlap_keys = copy(current_down_keys)
    if event_type == "all":
        return left_overlap_keys, fully_enclosed_keys, right_overlap_keys
    elif event_type == "left":
        return left_overlap_keys
    elif event_type == "right":
        return right_overlap_keys
    else:
        return None

def get_overlapping_keys(data):
    fully_overlapping_keys = []
    partial_overlapping_keys = []
    current_events = []
