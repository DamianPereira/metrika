# -*- coding: utf-8 -*-

from metrika.meter import Timer
from metrika.meter import FileMeter

from subprocess import STDOUT
from subprocess import call  # to launch benchs
import os

__author__ = 'Javier Pimás'


class Executor:
    def __init__(self):
        self.meters = []

    def measure_execution_time(self):
        self.meters.append(Timer())

    def measure_parsing_file(self, description, parser, filename):
        self.meters.append(FileMeter(description, parser, filename))


class CommandExecutor(Executor):
    def __init__(self, command_generator):
        super(CommandExecutor, self).__init__()
        self.command_generator = command_generator

    def run_with(self, contender, options, run_number):

        output = open(os.devnull, 'w')

        command = self.command_to_execute(contender, options)
        if options.verbose:
            print(self.command_to_execute(contender, options))

        # TODO: add nice support

        if not options.show_output:
            err_cut = " 2>&1"
            if run_number == 0:
                err_cut = " 2>&1"
            #else:
            #    err_cut = " 2>/dev/null"

            command = command + err_cut #+ " >/dev/null | head -n 25"
            # command = command + err_cut + " | head -n 25"
        for meter in self.meters:
            meter.start()

        self.do_execute(command)

        for meter in self.meters:
            meter.stop()

        return [meter.delta() for meter in self.meters]

    def do_execute(self, command):
        try:
            call(command, shell=True)
        except Exception as e:
            print("error executing %s: %s" % (self, e))

    def command_to_execute(self, contender, options):
        return self.command_generator(*[v.value() for v in contender.values])


