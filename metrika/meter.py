# -*- coding: utf-8 -*-

import time
import sys

__author__ = 'Javier Pimás'


class Meter(object):

    def __init__(self, unit_name):
        self.unit_name = unit_name
        self.start_measure = 0
        self.end_measure = 0
        self.measured = 0

    def __repr__(self):
        return "%d %s" % (self.measured, self.unit_name)

    def set(self, value):
        self.start_measure = value

    def done(self, value):
        self.end_measure = value
        self.measured = self.end_measure - self.start_measure
        return self.measured

    def delta(self):
        return self.measured


class Timer(Meter):
    def __init__(self):
        super(Timer, self).__init__("secs")

        if sys.platform == "win32":
            # On Windows, the best timer is time.clock()
            self.timer = time.clock
        else:
            # On most other platforms the best timer is time.time()
            self.timer = time.time

    def start(self):

        self.set(self.timer())

    def stop(self):
        return self.done(self.timer())


class FileMeter(Meter):
    def __init__(self, description, parser, filename):
        super(FileMeter, self).__init__(description)
        self.parser = parser
        self.filename = filename

    def start(self):
        pass

    def stop(self):
        with open(self.filename, 'r') as file:
            self.measured = self.parser(file)

