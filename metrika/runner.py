
# -*- coding: utf-8 -*-

import sys

__author__ = 'Javier Pimás'


def run_with(executor, contenders, options):

    results = {}
    invocations = options.invocations

    for contender in contenders:

        contender.setup()

        results[contender] = []

        #comparison.setup_for(contender)

        sys.stdout.write("running %d passes of %s. \n" % (invocations, str(contender))),

        for i in range(invocations):
            sys.stdout.write("%d... " % (i + 1))
            sys.stdout.flush()
            contender.setup()
            result = executor.run_with(contender, options, i)
            contender.teardown()

            results[contender].append(result)

        sys.stdout.write("\n")

    return results

