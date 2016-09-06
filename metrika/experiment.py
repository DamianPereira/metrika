# -*- coding: utf-8 -*-

import metrika.runner as runner
from metrika.executor import CommandExecutor
from metrika.reporter import Reporter
from metrika.plotter import Plotter

__author__ = 'Javier Pimás'


class Experiment:
    def __init__(self, name, suite):
        self.name = name
        self.suite = suite
        self.runner = runner
        self.measures = []
        self.reporter = None

    def __repr__(self):
        return self.name + ' exp'

    def restrict(self, arguments):
        return self.suite.restrict(arguments)

    def instances(self):
        return self.suite.instances()

    def invoke_with_command(self, command_generator):
        self.executor = CommandExecutor(command_generator)

    def measure_execution_time(self):
        self.measures.append('time')
        self.executor.measure_execution_time()

    def measure_parsing_file(self, description, parser, filename):
        self.measures.append(description)
        self.executor.measure_parsing_file(description, parser, filename)

    def run(self, arguments):
        contenders = self.suite.instances()
        return self.runner.run_with(self.executor, contenders, arguments)

    def set_report(self, configurator, name, description):
        self.reporter = Reporter(name, description)
        configurator(self.reporter)

    def set_plotter(self, configurator, name, description):
        self.plotter = Plotter(configurator, name, description)


    def use_generic_reporter(self):
        self.reporter = Reporter('', '')
        self.reporter.add_column('contender', lambda contender, _: contender)
        self.reporter.add_common_columns()
        self.reporter.sort_by(lambda row: row[0])

    def report(self, name, results, i):
        if self.reporter is None:
            self.use_generic_reporter()

        self.reporter.report(name, results, i)

    def plot(self, name, results, i):
        if self.plotter is None:
            self.use_generic_plotter()

        self.plotter.run_with(results, name, i)

