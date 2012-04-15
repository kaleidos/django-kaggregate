# -*- coding: utf-8 -*-

from .utils import Singleton

class Register(object):
    __metaclass__ = Singleton
    aggregators = {}

    def add(self, aggregator, prefix=""):
        self.aggregators[aggregators.uuid] = (aggregator, prefix)
