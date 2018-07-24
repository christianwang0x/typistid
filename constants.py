from misc import *

KEY_DOWN = DOWN = 0
KEY_UP = UP = 1
TIME_UNITS = 0.001
T = 0
K = 1
D = 2

KEYS_T = (('tab', 9),
          ('enter', 13),
          ('shift', 16),
          ('ctrl', 17),
          ('alt', 18),
          ('pause/break', 19),
          ('caps lock', 20),
          ('escape', 27),
          ('space', 32),
          ('page up', 33),
          ('page down', 34),
          ('end', 35),
          ('home', 36),
          ('left arrow', 37),
          ('up arrow', 38),
          ('right arrow', 39),
          ('down arrow', 40),
          ('insert', 45),
          ('delete', 46),
          ('0', 48),
          ('1', 49),
          ('2', 50),
          ('3', 51),
          ('4', 52),
          ('5', 53),
          ('6', 54),
          ('7', 55),
          ('8', 56),
          ('9', 57),
          ('a', 65),
          ('b', 66),
          ('c', 67),
          ('d', 68),
          ('e', 69),
          ('f', 70),
          ('g', 71),
          ('h', 72),
          ('i', 73),
          ('j', 74),
          ('k', 75),
          ('l', 76),
          ('m', 77),
          ('n', 78),
          ('o', 79),
          ('p', 80),
          ('q', 81),
          ('r', 82),
          ('s', 83),
          ('t', 84),
          ('u', 85),
          ('v', 86),
          ('w', 87),
          ('x', 88),
          ('y', 89),
          ('z', 90),
          ('left window key', 91),
          ('right window key', 92),
          ('select key', 93),
          ('numpad 0', 96),
          ('numpad 1', 97),
          ('numpad 2', 98),
          ('numpad 3', 99),
          ('numpad 4', 100),
          ('numpad 5', 101),
          ('numpad 6', 102),
          ('numpad 7', 103),
          ('numpad 8', 104),
          ('numpad 9', 105),
          ('multiply', 106),
          ('add', 107),
          ('subtract', 109),
          ('decimal point', 110),
          ('divide', 111),
          ('f1', 112),
          ('f2', 113),
          ('f3', 114),
          ('f4', 115),
          ('f5', 116),
          ('f6', 117),
          ('f7', 118),
          ('f8', 119),
          ('f9', 120),
          ('f10', 121),
          ('f11', 122),
          ('f12', 123),
          ('num lock', 144),
          ('scroll lock', 145),
          ('semi-colon', 186),
          ('equal sign', 187),
          ('comma', 188),
          ('dash', 189),
          ('period', 190),
          ('forward slash', 191),
          ('grave accent', 192),
          ('open bracket', 219),
          ('back slash', 220),
          ('close braket', 221),
          ('single quote', 222))

KEYS = dict(KEYS_T)
IKEYS = invert_dict(KEYS)

KEYPRESS_TEMPLATE = ("code: {code}\nkey: {key}\nstart_index: {start_index}\n"
                     "stop_index: {stop_index}\nstart_time: {start_time}\n"
                     "stop_time: {stop_time}\nchildren: {children}\n"
                     "step_children: {step_children}\nparents: {parents}\n"
                     "step_parents: {step_parents}\n")

BASIC_CONSOLE_TEMPLATE = "Usage: {0} compare file1 file2 file3 or\n" \
                         "       {0} visualize data.json"

AUTHOR_TEMPLATE = "Author of {0} is same as author of {1}."
