# -*- coding: utf-8 -*-

import texttable as tt
from math import sqrt

__author__ = 'Javier Pimás'


def report(results):

    tab = tt.Texttable()
    tab.header(['Benchmark', 'Input', 'Average', 'std dev %', 'std dev', 'runs', 'discarded'])

    tab.set_cols_align(['r','r', 'r','r', 'r', 'r', 'r'])
    tab.set_deco(tab.HEADER | tab.VLINES)

    for benchmark, measures in sorted(results.items()):
        report_benchmark(tab, benchmark, measures)

    table = tab.draw()
    print (table)


def report_benchmark(tab, benchmark, measures):

    trimmed = trim_ends(sorted(measures), 0.1)
    runs = len(trimmed)
    average = sum(trimmed) / runs
    stddev  = sqrt(sum([(measure - average)**2 for measure in trimmed]))
    stddev_relative = stddev / average * 100
    tab.add_row([benchmark.name(), benchmark.input, average, "%2.2f %%" % stddev_relative, stddev, len(measures), len(measures) - runs])

    tab.set_cols_width([35, 10, 10, 10, 10, 10, 10])


def trim_ends(sorted_list, proportion_to_cut):

    size = len(sorted_list)
    left = int(proportion_to_cut * size)
    right = size - left

    return sorted_list[left:right]
