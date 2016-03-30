
# -*- coding: utf-8 -*-

import sys

__author__ = 'Javier Pimás'


def start(benchmarks, timer):

    runs = 5
    results = {}

    # random.shuffle(self.benchmarks)

    for benchmark in benchmarks:
        results[benchmark] = []

        benchmark.global_setup()

        sys.stdout.write("running %d passes of %s. \n" % (runs, str(benchmark))),

        for i in range(runs):
            sys.stdout.write("%d... " % (i + 1))
            sys.stdout.flush()
            benchmark.setup()
            benchmark.run_using(timer, i)
            benchmark.teardown()

            results[benchmark].append(timer.delta())

        benchmark.global_teardown()
        sys.stdout.write("\n")
    return results

