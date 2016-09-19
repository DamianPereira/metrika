#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
if sys.version_info < (3, 4):
    raise Exception("must use python 3.4 or greater")

from metrika.engine import Engine
import glob
__author__ = 'Javier Pimás'



if __name__ == '__main__':

    engine = Engine()

    modules = []
    for module_name in glob.glob("measure_*.py"):
        modules.append(__import__(module_name[:-3]))

    for module in modules:
        module.configure(engine)

    engine.go()

# example of how to run:
# $> python -m metrika run join-speed test
