from functools import reduce
from operator import getitem


def grab_data(iris_native, global_name, data=None, *keys):
    if not data:
        data = []
    iter = iris_native.iterator(global_name, *keys)
    for k, v in iter.items():
        n_keys = keys + (k,)
        data.append((n_keys, v))
        grab_data(iris_native, global_name, data, *n_keys)
    return data


def get_tree(tree, mappings):
    return reduce(getitem, mappings, tree)


def set_tree(tree, mappings, val):
    mps = []
    for m in mappings[:-1]:
        mps.append(m)
        mps.append('items')
    get_tree(tree, mps)[mappings[-1]] = dict(value=val, items=dict())


def generate_tree(data):
    tree = {}
    for item in data:
        set_tree(tree, list(item[0]), item[1])
    return tree