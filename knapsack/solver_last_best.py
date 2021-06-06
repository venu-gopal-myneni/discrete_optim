#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
from operator import attrgetter
from collections import namedtuple
import pprint
import time
Item = namedtuple("Item", ['index', 'value', 'weight', 'vw_ratio'])


def find_greedy_sol(capacity, items_sor, out_list, method):
    weight = 0
    value = 0
    for item in items_sor:
        if (item.weight + weight <= capacity):
            out_list[item.index] = 1
            value += item.value
            weight += item.weight
        else:
            if method == "weight":
                return value, out_list, round(weight/capacity, 2)
    return value, out_list, round(weight/capacity, 2)


adict = {}


def dyprg(capacity, items, taken, start_time, time_limit):
    # build empty matrix
    # i=capac,j = items
    matrix = []
    for row in range(0, capacity+1):
        column = []
        for col in range(0, len(items)+1):
            column.append(0)
        matrix.append(column)
    for col_pos in range(1, len(items)+1):
        item = items[col_pos-1]

        for row_pos in range(1, capacity+1):
            if time.time()-start_time > time_limit:
                return -1, []
            if item.weight <= row_pos:
                key1 = str(row_pos)+"-"+str(col_pos-1)
                key2 = str(row_pos-item.weight)+"-"+str(col_pos-1)
                if key1 in adict:
                    case1 = adict[key1]
                else:
                    case1 = matrix[row_pos][col_pos-1]
                    adict[key1] = case1
                if key2 in adict:
                    case2 = item.value+adict[key2]
                else:
                    case2 = item.value + matrix[row_pos-item.weight][col_pos-1]
                    adict[key2] = matrix[row_pos-item.weight][col_pos-1]
                matrix[row_pos][col_pos] = max(case1, case2)
                key3 = str(row_pos)+"-"+str(col_pos)
                adict[key3] = max(case1, case2)
            else:
                key4 = str(row_pos)+"-"+str(col_pos-1)
                key5 = str(row_pos)+"-"+str(col_pos)
                if key4 in adict:
                    matrix[row_pos][col_pos] = adict[key4]
                    adict[key5] = matrix[row_pos][col_pos]
                else:
                    matrix[row_pos][col_pos] = matrix[row_pos][col_pos-1]
                    adict[key4] = matrix[row_pos][col_pos-1]
                    adict[key5] = matrix[row_pos][col_pos]

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
    return matrix[capacity][len(items)], taken


def greedy(capacity, items, taken):
    # sort by value
    items_val = sorted(items, key=attrgetter('value'), reverse=True)
    # sort by weight
    items_wei = sorted(items, key=lambda x: x.weight)
    # sort by vw_ratio
    items_vw = sorted(items, key=lambda x: x.vw_ratio, reverse=True)

    taken_val, list_val, perf_val = find_greedy_sol(
        capacity, items_val, copy.copy(taken), "value")
    taken_wei, list_wei, perf_wei = find_greedy_sol(
        capacity, items_wei, copy.copy(taken), "weight")
    taken_vw, list_vw, perf_vw = find_greedy_sol(
        capacity, items_vw, copy.copy(taken), "vw_ratio")
    #print(f" val : {taken_val}-{perf_val}, wei : {taken_wei}-{perf_wei} ,vw : {taken_vw}-{perf_vw}")
    if taken_val >= taken_wei and taken_val >= taken_vw:
        return taken_val, list_val
    elif taken_wei >= taken_val and taken_wei >= taken_vw:
        return taken_wei, list_wei
    else:
        return taken_vw, list_vw


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(
            Item(i-1, int(parts[0]), int(parts[1]), round(int(parts[0])/int(parts[1]), 2)))

    # a trivial algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    taken = [0]*len(items)

    #value, taken = greedy(capacity, items, taken)
    start_time = time.time()
    time_limit = 300
    value, taken = dyprg(capacity, items, copy.copy(
        taken), start_time, time_limit)
    if value == -1:
        value, taken = greedy(capacity, items, taken)

    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')
