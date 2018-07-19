from misc import *

DOWN = 0
UP = 1
TIME_UNITS = 0.001
T = 0
K = 1
D = 2

KEYS = {"8": 56,
        "6": 54,
        "u": 85,
        "open bracket": 219,
        "k": 75,
        "backspace": 8,
        "left window key": 91,
        "enter": 13,
        "x": 88,
        "5": 53,
        "f2": 113,
        "page up": 33,
        "scroll lock": 145,
        "b": 66,
        "forward slash": 191,
        "9": 57,
        "r": 82,
        "numpad 9": 105,
        "g": 71,
        "numpad 1": 97,
        "grave accent": 192,
        "7": 55,
        "semi-colon": 186,
        "c": 67,
        "numpad 7": 103,
        "2": 50,
        "num lock": 144,
        "f6": 117,
        "numpad 8": 104,
        "down arrow": 40,
        "caps lock": 20,
        "home": 36,
        "f": 70,
        "tab": 9,
        "0": 48,
        "page down": 34,
        "p": 80,
        "v": 86,
        "escape": 27,
        "a": 65,
        "y": 89,
        "close braket": 221,
        "f11": 122,
        "up arrow": 38,
        "w": 87,
        "s": 83,
        "e": 69,
        "f7": 118,
        "ctrl": 17,
        "comma": 188,
        "n": 78,
        "f10": 121,
        "end": 35,
        "add": 107,
        "q": 81,
        "pause/break": 19,
        "h": 72,
        "single quote": 222,
        "4": 52,
        "numpad 5": 101,
        "m": 77,
        "alt": 18,
        "delete": 46,
        "f8": 119,
        "multiply": 106,
        "insert": 45,
        "l": 76,
        "f5": 116,
        "numpad 2": 98,
        "f3": 114,
        "o": 79,
        "period": 190,
        "f4": 115,
        "subtract": 109,
        "select key": 93,
        "back slash": 220,
        "d": 68,
        "3": 51,
        "numpad 6": 102,
        "i": 73,
        "f9": 120,
        "numpad 3": 99,
        "j": 74,
        "f1": 112,
        "right arrow": 39,
        "numpad 0": 96,
        "f12": 123,
        "right window key": 92,
        "z": 90,
        "numpad 4": 100,
        "t": 84,
        "divide": 111,
        "shift": 16,
        "left arrow": 37,
        "dash": 189,
        "1": 49,
        "decimal point": 110,
        "equal sign": 187,
        "space": 32}

IKEYS = invert_dict(KEYS)

KEYPRESS_TEMPLATE = "code: {code}\nkey: {key}\nstart_index: {start_index}\nstop_index: {stop_index}\nstart_time: {start_time}\nstop_time: {stop_time}\nchildren: {children}\nstep_children: {step_children}\nparents: {parents}\nstep_parents: {step_parents}\n"