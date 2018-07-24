# Returned inverted dictionary
def invert_dict(d):
    inverted_dict = dict()
    for (key, val) in d.items():
        inverted_dict[val] = key
    return inverted_dict


# Get all possible slices of length min_slice_len to
# max_slice_len with the upper bound being max_index
def get_slices(min_slice_len, max_slice_len, max_index):
    slices = []
    for slice_len in range(min_slice_len, max_slice_len+1):
        for index in range(max_index+1 - slice_len):
            slices.append(slice(index, index + slice_len, 1))
    return slices
