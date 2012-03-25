class Register(object):
    __instance = None
    aggregators = {}

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance

    def add(self, key, aggregator):
        self.aggregators[key] = aggregator
