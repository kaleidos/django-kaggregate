import itertools
from .models import *

class AggregationKeyAlreadyExists(Exception):
    pass

class Aggregator:
    def add_aggregation(self, key, *args, **kwargs):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError


class QSAggregatorFunc(Aggregator):
    qs = None
    funcs = {}

    def __init__(self, qs, **kwargs):
        self.qs = qs

    def add_aggregation(self, key, agg_obj):
        if key in self.funcs.keys():
            raise AggregationKeyAlreadyExists()
        else:
            self.funcs[key] = agg_obj

    def run(self):
        for item in self.qs.aggregate(**self.funcs).iteritems():
            try:
                agg = KAggregate.objects.get(key=item[0])
            except KAggregate.DoesNotExist:
                agg = KAggregate(key=item[0])
            agg.value = item[1]
            agg.save()
        

class QSAggregator(Aggregator):
    qs = None
    funcs = {}

    def __init__(self, qs, **kwargs):
        self.qs = qs

    def add_aggregation(self, key, reduce_func, map_func=None, final_func=None):
        if key in self.funcs.keys():
            raise AggregationKeyAlreadyExists()
        else:
            self.funcs[key] = {}
            self.funcs[key]['reduce_func'] = reduce_func

            if map_func == None:
                self.funcs[key]['map_func'] = lambda x: x
            else:
                self.funcs[key]['map_func'] = map_func

            if final_func == None:
                self.funcs[key]['final_func'] = lambda qs, x: x
            else:
                self.funcs[key]['final_func'] = final_func

    def run(self):
        for key in self.funcs.keys():
            self.funcs[key]['tmpvalue'] = 0

        first = True
        for item in self.qs:
            for key in self.funcs.keys():
                if first:
                    self.funcs[key]['tmpvalue'] = self.funcs[key]['map_func'](item)
                    first = False
                else:
                    self.funcs[key]['tmpvalue'] = self.funcs[key]['reduce_func'](self.funcs[key]['tmpvalue'], self.funcs[key]['map_func'](item))

        for key in self.funcs.keys():
            self.funcs[key]['tmpvalue']= self.funcs[key]['final_func'](self.qs, self.funcs[key]['tmpvalue'])

        for key in self.funcs.keys():
            try:
                agg = KAggregate.objects.get(key=key)
            except KAggregate.DoesNotExist:
                agg = KAggregate(key=key)
            agg.value = self.funcs[key]['tmpvalue']
            agg.save()
