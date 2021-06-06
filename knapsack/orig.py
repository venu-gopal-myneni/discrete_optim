import time
from collections import namedtuple
import pprint
import numpy as np
Item = namedtuple("Item", ['index', 'value', 'weight', 'vw_ratio'])
adict = {}
adict = {}


def get_val(items, row_pos, col_pos):
    item = items[col_pos-1]
    key3 = str(row_pos)+"-"+str(col_pos)
    if key3 in adict:
        return adict[key3]
    if item.weight <= row_pos:

        case1 = get_val(items, row_pos, col_pos-1)
        case2 = item.value+get_val(items, row_pos-item.weight, col_pos-1)
        val = max(case1, case2)

        adict[key3] = max(case1, case2)
    else:

        val = get_val(items, row_pos, col_pos-1)
        adict[key3] = val
    return val


def dyprg(capacity, items, taken, start_time, time_limit):
    # build empty matrix
    # i=capac,j = items
    matrix = []
    for row_pos in range(0, capacity+1):
        key = str(row_pos)+"-"+str(0)
        adict[key] = 0
    for col_pos in range(0, len(items)+1):
        key = str(0)+"-"+str(col_pos)
        adict[key] = 0
    # for row in range(0, capacity+1):
    #     column = []
    #     for col in range(0, len(items)+1):
    #         column.append(0)
    #     matrix.append(column)
    matrix = np.zeros((capacity+1, len(items)+1))
    for col_pos in range(1, len(items)+1):
        # drop all previous except last but one
        if col_pos >= 2:
            removes = []
            for key in adict:
                key_list = key.split("-")
                if int(key_list[1]) < col_pos-1:
                    removes.append(key)
            for key in removes:
                del adict[key]

        for row_pos in range(1, capacity+1):
            # print(adict)
            if time.time()-start_time > time_limit:
                return -1, []

            matrix[row_pos][col_pos] = get_val(items, row_pos, col_pos)

    # pprint.pprint(matrix)

    row_pos, col_pos = capacity, len(items)
    for i in range(0, len(items)):
        if matrix[row_pos][col_pos] == matrix[row_pos][col_pos-1]:
            taken[col_pos-1] = 0
            col_pos -= 1
        else:
            taken[col_pos-1] = 1

            row_pos = row_pos-items[col_pos-1].weight
            col_pos -= 1
    print(f"adict len : {len(adict)}")
    return int(matrix[capacity][len(items)]), taken


if __name__ == "__main__":
    capacity = 7
    items = [Item(0, 5, 4, 5/4), Item(1, 6, 5, 6/5), Item(2, 3, 2, 3/2)]
    items = [Item(0, 16, 2, 16/2), Item(1, 19, 3, 19/3),
             Item(2, 23, 4, 23/4), Item(3, 28, 5, 28/5)]
    taken = [0, 0, 0, 0]
    print(dyprg(capacity, items, taken, time.time(), 300))
