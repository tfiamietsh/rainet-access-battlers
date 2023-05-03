import re
from math import floor
from misc.constants import IMAGE_SIZE, CARD_SIZE, FIELD_START_POS
from threading import Thread
from rainet import __DEBUG__MODE__


def inverted(size, offset):
    return tuple(IMAGE_SIZE[idx] - size[idx] - offset[idx] for idx in range(2))


def pos_to_indices(pos):
    return (pos[1] - FIELD_START_POS[1]) // CARD_SIZE[1], (pos[0] - FIELD_START_POS[0]) // CARD_SIZE[0]


def indices_to_pos(indices):
    return CARD_SIZE[0] * indices[1] + FIELD_START_POS[0], CARD_SIZE[1] * indices[0] + FIELD_START_POS[1]


def re_sub_a_z(text):
    return re.sub('[a-z]', '', text)


def re_sub_plus(text):
    return re.sub('\+', '', text)


def re_sub_minus(text):
    return re.sub('-', '', text)


def inverse_manhattan_distance(pair1, pair2):
    return 1 / (abs(pair1[0] - pair2[0]) + abs(pair1[1] - pair2[1]))


def is_pos_in_rect(pos, rect):
    return 0 <= pos[0] - rect[0] <= rect[2] and 0 <= pos[1] - rect[1] <= rect[3]


def correct_percent_str(value):
    s = str(value)
    while len(s) < 3:
        s = ' ' + s
    return s


def round(value, multiple_of):
    return int(floor((value + multiple_of / 2) / multiple_of) * multiple_of)


def cyclic_increment(value, limit):
    return (value + 1) % limit


def cyclic_decrement(value, limit):
    return (value - 1) % limit


def start_daemon_thread(target, args=()):
    Thread(target=target, args=args, daemon=True).start()


def try_else(try_func, except_func=lambda: True, else_func=lambda: True):
    try:
        result = try_func()
    except Exception as e:
        if __DEBUG__MODE__:
            print(e)
        except_func()
        return e
    else:
        else_func()
        return result


def str_to_pair_list(s):
    if s is None or s == '':
        raise Exception
    for ch in '[(,)]':
        s = s.replace(ch, '')
    s = s.split()
    return list(zip([int(s[i]) for i in range(0, len(s), 2)], [int(s[i]) for i in range(1, len(s), 2)]))
