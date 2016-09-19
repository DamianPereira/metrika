# -*- coding: utf-8 -*-

import itertools
from metrika.contender import Contender
from metrika.variable import *

__author__ = 'Javier Pimás'


class Suite:
    def __init__(self, name=""):
        self.name = name
        self.variables = []

    def add_variable_from_dict(self, name, values):
        values = [NamedValue(name, value) for name, value in values.items()]
        self.variables.append(Variable(name, values))

    def add_variable_from_list(self, name, values):
        values = [AnonValue(value) for value in values]
        self.variables.append(Variable(name, values))

    def restrict(self, arguments):
        # for arg in arguments:
        #    if self.typical_parameters[arg] is None:
        #        args.append(arg)
        #    else:
        #        args.append(self.typical_parameters[arg])
        if arguments.restrict is not None:
            for restriction in arguments.restrict.split(','):
                (var, value) = restriction.split('=')
                variable = next(x for x in self.variables if x.name == var)
                variable.restrict_to(value)

    def instances(self):
        names = [var.name for var in self.variables]
        values = [var.values for var in self.variables]

        tuples = itertools.product(*values)

        return [Contender(names, variation) for variation in list(tuples)]

