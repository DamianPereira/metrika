
# -*- coding: utf-8 -*-

import sys

__author__ = 'Javier Pimás'


def start(executors, options):

    results = {}
    invocations = options.invocations

    for executor in executors:
        results[executor] = []

        executor.global_setup()

        sys.stdout.write("running %d passes of %s. \n" % (invocations, str(executor))),

        for i in range(invocations):
            sys.stdout.write("%d... " % (i + 1))
            sys.stdout.flush()
            executor.setup()
            executor.run(options, i)
            executor.teardown()

            results[executor].append(executor.gather_results())

        executor.global_teardown()
        sys.stdout.write("\n")
    return results

