# -*- coding: utf-8 -*-

import time
import sys
import metrika_meter

__author__ = 'Javier Pimás'


class MetrikaTimer(metrika_meter.MetrikaMeter):

    def __init__(self):
        super(MetrikaTimer, self).__init__("ticks")

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

