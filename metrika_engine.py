
import metrika_runner
import metrika_reporter
import metrika_database

import argparse
import socket

import sys


class MetrikaEngine:
    def __init__(self, outliner):
        # hook to be able to have 'run' as default command
        argparse.ArgumentParser.set_default_subparser = set_default_subparser

        self.outliner = outliner
        self.arguments = self.parse_arguments()
        self.database = metrika_database.MetrikaDatabase(self.arguments.testbed)

    def go(self):
        self.arguments.func()

    @property
    def machine_name(self):
        return socket.gethostname()

    def run_command(self):
        self.run()
        if not self.arguments.quiet:
            self.report()

    def report_command(self):
        self.report()

    def plot_command(self):
        self.plot()

    def filter_benchmarks(self):
        pass

    def run(self):

        if self.arguments.bench:
            self.filter_benchmarks()

        plan = self.outliner.generate_fixture_for(self)

        if self.arguments.force:
            selected = plan
        else:
            selected = self.database.reject_already_measured_in(plan)

        done = [x for x in plan if x not in selected]

        print("benchs to run: " + str(selected))
        print("benchs skipped: " + str(done))

        old_results = self.database.measured_results_of(done)
        new_results = metrika_runner.start(selected, self.arguments)

        all_results = dict(old_results)
        all_results.update(new_results)
        self.database.save(new_results)

    def report(self):
        plan = self.outliner.generate_fixture_for(self)
        results = self.database.measured_results_of(plan)
        metrika_reporter.report(results)

    def plot(self):
        plan = self.outliner.generate_fixture_for(self)
        results = self.database.measured_results_of(plan)
        self.outliner.plot(results, self.database.testbed)

    def parse_arguments(self):
        parser = argparse.ArgumentParser(prog='Metrika', description='A scientifically rigorous measurement tool')
        parser.add_argument('-v', '--verbose', action='store_true', help='show more output')
        parser.add_argument('-b', '--bench', help='restrict to only specified benchs')
        parser.add_argument('--testbed', default=self.machine_name, help='name for the platform where we are running')
        subparsers = parser.add_subparsers(help='possible commands')

        parser_run = subparsers.add_parser('run', help='measure runs')
        parser_run.add_argument('-I', '--invocations', type=int, default=5, help='number of invocations')
        parser_run.add_argument('-i', type=int, default=5, help='number of iterations')
        parser_run.add_argument('-f', '--force', action='store_true',
                                help='force measuring again even if results are already in database')
        parser_run.add_argument('-q', '--quiet', action='store_true', help='do not show summary of results')
        parser_run.add_argument('-s', '--show-output', action='store_true',
                                help='show output of programs being run in stdout')
        parser_run.add_argument('-e', '--hide-errors', action='store_true',
                                help='hide errors of programs being run')
        parser_run.add_argument('series', help='choose which series to run')
        parser_run.set_defaults(func=self.run_command)

        parser_report = subparsers.add_parser('report', help='report measures given results database, without running\n'
                                                             ' benchs again')
        parser_report.add_argument('series', help='choose which series to report')
        parser_report.set_defaults(func=self.report_command)

        parser_plot = subparsers.add_parser('plot', help='plot results from database contents')
        parser_plot.add_argument('series', help='choose which series to plot')
        parser_plot.set_defaults(func=self.plot_command)

        parser.set_default_subparser('run')
        return parser.parse_args()


def set_default_subparser(self, name, args=None):
    """default subparser selection. Call after setup, just before parse_args()
    name: is the name of the subparser to call by default
    args: if set is the argument list handed to parse_args()

    , tested with 2.7, 3.2, 3.3, 3.4
    it works with 2.6 assuming argparse is installed
    """
    subparser_found = False
    for arg in sys.argv[1:]:
        if arg in ['-h', '--help']:  # global help if no subparser
            break
    else:
        for x in self._subparsers._actions:
            if not isinstance(x, argparse._SubParsersAction):
                continue
            for sp_name in x._name_parser_map.keys():
                if sp_name in sys.argv[1:]:
                    subparser_found = True
        if not subparser_found:
            # insert default in first position, this implies no
            # global options without a sub_parsers specified
            if args is None:
                sys.argv.insert(1, name)
            else:
                args.insert(0, name)