# -*- coding: utf-8 -*-

from .utils import Singleton

class Register(object):
    __metaclass__ = Singleton
    aggregators = {}

    def add(self, aggregator, prefix=""):
        self.aggregators[aggregator.uuid] = (aggregator, prefix)

register = Register()
add = register.add

__all__ = ['add', 'register']
