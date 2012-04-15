# -*- coding: utf-8 -*-

from kaggregate.utils import Singleton

class BaseStorageBackend(object):
    __metaclass__ = Singleton

    def save(self, key, value):
        """
        Method for save or update current value for key.
        """
        raise NotImplementedError

    def current_value(self, key, default=None):
        """
        Method for obtain current value for key.
        """
        raise NotImplementedError

    def flush(self, key):
        """
        Flush a result for a key.
        """
        raise NotImplementedError

    def flushall(self):
        """
        Flush all saved results.
        """
        raise NotImplementedError
