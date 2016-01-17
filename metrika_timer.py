# -*- coding: utf-8 -*-

import time
import sys

__author__ = 'Javier Pimás'


class MetrikaTimer(object):

    def __init__(self):

        if sys.platform == "win32":
            # On Windows, the best timer is time.clock()
            self.timer = time.clock
        else:
            # On most other platforms the best timer is time.time()
            self.timer = time.time

    def start(self):

        self.prev_tick = self.timer()

    def stop(self):
        self.elapsed = self.timer() - self.prev_tick
        return self.elapsed

    def elapsed(self):
        self.elapsed