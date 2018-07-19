def invert_dict(d):
    inverted_dict = dict()
    for (key, val) in d.items():
        inverted_dict[val] = key
    return inverted_dict

