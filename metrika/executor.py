# -*- coding: utf-8 -*-

from subprocess import STDOUT
from subprocess import call  # to launch benchs
import os

__author__ = 'Javier Pimás'


class MetrikaExecutor:
    def __init__(self, bench, contender):
        self.bench = bench
        self.contender = contender

    def global_setup(self):
        pass

    def setup(self):
        pass

    def teardown(self):
        pass

    def global_teardown(self):
        pass

    def run(self, options, run_number):

        output = open(os.devnull, 'w')

        command = self.command_to_execute(options)
        if options.verbose:
            print(self.command_to_execute(options))

        if not options.show_output:
            if run_number == 0:
                err_cut = " 2>&1"
            else:
                err_cut = " 2>/dev/null"

            command = command + err_cut + " >/dev/null | head -n 25"
            # command = command + err_cut + " | head -n 25"

        self.do_execute(command)

    def do_execute(self, command):
        try:
            call(command, shell=True)
        except Exception as e:
            print("error executing %s: %s" % (self, e))

    def command_to_execute(self, options):
        return self.contender.command_to_execute(self.bench, options)

    def __repr__(self):
        return "%s on %s" % (str(self.bench), str(self.contender))

    def __lt__(self, other):
        return self.identity() < other.identity()

    def identity(self):
        return ' '.join([str(self.bench), str(self.contender)])
