# -*- coding: utf-8 -*-

import statistics as s
import datetime
import platform
import socket

try:
    import texttable as tt
except ImportError:
    print("please install texttable to show results (pip3 install --user texttable")

try:
    import psutil
except ImportError:
    print("please install psutil to show results (sudo apt-get install python3-psutil?")

try:
    from cpuinfo import cpuinfo
except ImportError:
    print("please install cpuinfo to show results (pip3 install --user py-cpuinfo")

__author__ = 'Javier Pimás'


class Reporter:
    def __init__(self, name, description):
        self.columns = []
        self.name = name
        self.description = description
        self.sorter = None

    def add_column(self, name, gen, size=None):
        self.columns.append(ColumnDescriptor(name, gen, size))

    def add_median(self):
        self.add_column('median', lambda _, results: s.median(results))

    def add_stddev(self):
        self.add_column('std dev', lambda _, results: s.pstdev(results))

    def add_stdev_rel(self):
        self.add_column('std dev %', lambda _, results: "%2.2f %%" % (s.pstdev(results) * 100 / s.median(results)))

    def add_runs(self):
        self.add_column('runs', lambda _, res: len(res))

    def add_common_columns(self):
        self.add_median()
        self.add_stdev_rel()
        self.add_runs()

    def sort_by(self, sorter):
        self.sorter = sorter

    def report(self, title, results, i):
        print("-----")
        print(title)
        print("-----")

        tab = tt.Texttable()
        tab.header([c.name for c in self.columns])

        tab.set_cols_align(['r' for _ in self.columns])
        tab.set_deco(tab.HEADER | tab.VLINES)

        rows = []
        for experiment, contenders in sorted(results.items()):
            for contender, measures in contenders.items():
                values = [measure[i] for measure in measures]
                rows.append([c.value(contender, values) for c in self.columns])

        if self.sorter is not None:
            rows = sorted(rows, key=self.sorter)

        for row in rows:
            tab.add_row(row)

        tab.add_row(["." * c.size for c in self.columns])
        tab.set_cols_width([c.size for c in self.columns])

        table = tab.draw()
        print(table)

        print("\nresults obtained at %s in the following system:\n" % datetime.datetime.now())
        print(get_system_info())


class ColumnDescriptor:
    def __init__(self, name, gen, size=None):
        self.name = name
        self.gen = gen
        self.size = size if size is not None else len(name)

    def value(self, contender, measures):
        return self.gen(contender, measures)


def get_system_info():
    info = 'testbed: ' + socket.gethostname()
    info += '\nos:  %s (%s-%s-%s)' % (' '.join(platform.dist()),
                                platform.system(), platform.release(), platform.machine()) + '.'

    cpu = cpuinfo.get_cpu_info()
    mibi = 1024*1024
    giga = 1000*1000*1000
    info += "\n" + "cpu: %s (@%.2f GHz), %s l2 cache, " % (cpu['brand'], cpu['hz_actual_raw'][0]/giga, cpu['l2_cache_size'])
    info += "%d logical cores (%d physical)" % (psutil.cpu_count(), psutil.cpu_count(False))
    mem = psutil.virtual_memory()
    info += "\nmem: %d MB phys, %d MB free" % (mem.total/mibi, mem.free/mibi)

    return info

