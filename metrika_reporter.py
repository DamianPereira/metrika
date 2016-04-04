# -*- coding: utf-8 -*-

import platform
import time
from math import sqrt

try:
    import texttable as tt
except ImportError:
    print("please install texttable to show results (sudo apt-get install python3-texttable?")

try:
    import psutil
except ImportError:
    print("please install psutil to show results (sudo apt-get install python3-psutil?")

try:
    from cpuinfo import cpuinfo
except ImportError:
    print("please install cpuinfo to show results (pip3 install py-cpuinfo")


__author__ = 'Javier Pimás'


def report(results):
    tab = tt.Texttable()
    tab.header(['Benchmark', 'Input', 'Average', 'std dev %', 'std dev', 'runs', 'discarded'])

    tab.set_cols_align(['r', 'r', 'r', 'r', 'r', 'r', 'r'])
    tab.set_deco(tab.HEADER | tab.VLINES)

    grouped = {}

    for benchmark in results.keys():
        if benchmark.name() not in grouped:
            grouped[benchmark.name()] = []

        grouped[benchmark.name()].append(benchmark)

    #for benchmark, measures in sorted(results.items()):
    for name, group in sorted(grouped.items()):
        for benchmark in sorted(group):
            measures = results[benchmark]
            report_benchmark(tab, benchmark, measures)

        tab.add_row(("··········", "······", "······", "·····", "·······", "·····", "······"))

    table = tab.draw()
    print(table)

    context = '\n%s-%s-%s on %s' % (platform.system(), platform.release(), platform.machine(),
                                    time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())) + '.'

    print(context)
    print("%d logical cores (%d physical)" % (psutil.cpu_count(), psutil.cpu_count(False)))
    print(str(psutil.virtual_memory()))

    print("cpuinfo: %s" % (str(cpuinfo.get_cpu_info())))


def report_benchmark(tab, executor, measures):
    trimmed = trim_ends(sorted(measures), 0.1)
    runs = len(trimmed)
    average = sum(trimmed) / runs
    squared = [(measure - average) ** 2 for measure in trimmed]
    stddev = sqrt(sum(squared)/runs)
    stddev_relative = stddev / average * 100

    tab.add_row([str(executor.bench), str(executor.contender), average, "%2.2f %%" % stddev_relative, stddev, len(measures),
                 len(measures) - runs])

    tab.set_cols_width([50, 10, 8, 8, 8, 7, 7])


def trim_ends(sorted_list, proportion_to_cut):
    size = len(sorted_list)
    left = int(proportion_to_cut * size)
    right = size - left

    return sorted_list[left:right]
