# -*- coding: utf-8 -*-

import functools

def as_map_reduce(key):
    def _wrapper(method):
        method._kaggregator_mode = 'map-reduce'
        method._kaggregator_key = key
        return method
    return _wrapper
