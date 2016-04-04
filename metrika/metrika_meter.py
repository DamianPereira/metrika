# -*- coding: utf-8 -*-


__author__ = 'Javier Pimás'


class MetrikaMeter(object):

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