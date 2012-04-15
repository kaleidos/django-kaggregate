# -*- coding: utf-8 -*-

import uuid
import types

class MetaAggregator(type):
    def __new__(cls, name, bases, attrs):
        new_class = super(MetaAggregator, cls).__new__(cls, name, bases, attrs)
        new_class.add_to_class("uuid", property(lambda self: self._uuid))
        return new_class

    def __call__(cls, *args, **kwargs):
        """
        Ensure new uuid for every created instance.
        """

        instance = super(MetaAggregator, cls).__call__(*args, **kwargs)
        instance._uuid = str(uuid.uuid4())
        return instance
    
    def add_to_class(cls, name, value):
        if hasattr(value, 'contribute_to_class'):
            value.contribute_to_class(cls, name)
        else:
            setattr(cls, name, value)


class BaseAggregator(object):
    """
    Base class for all aggregators.
    """

    __metaclass__ = MetaAggregator
    _cached_methods = {}

    def objects(self):
        """
        Main method for get objects. The return object
        must be a iterator or generator object.
        """
        raise NotImplementedError

    def _get_methods(self, type_key):
        methods = []
        for attr_name in dir(self):
            attr = getattr(self, attr_name)

            if not isinstance(attr, types.MethodType):
                continue

            if not hasattr(attr, '_kaggregator_mode'):
                continue

            if attr._kaggregator_mode != type_key:
                continue

            methods.append((attr._kaggregator_key, attr()))
        return methods

    def map_reduce_methods(self):
        """
        Returns all map reduce methods.
        """

        return self._get_methods("map-reduce")

    def django_aggregators_methods(self):
        """
        Return all django aggregators methods.
        """

        return self._get_methods("django-aggregate")

    def run(self, prefix=""):
        map_reduce_methods, results = {}, {}

        for key, method in self.map_reduce_methods():
            map_reduce_methods[key] = {}

            if "reduce" not in method:
                continue

            map_reduce_methods[key]['reduce'] = method['reduce']
            map_reduce_methods[key]['map'] = lambda x: x \
                if "map" not in method else method['map']
            map_reduce_methods[key]['final'] lambda qs, x: x\
                if "final" not in method else method['final']

            results[key] = 0

        # make all map reduce registred operations
        first = True
        for obj in self.objects():
            for key, method in map_reduce_methods.iteritems():
                if first:
                    results[key], first = method['map'](obj), False
                    continue
                
                results[key] = method['reduce'](results[key], method['map'](obj))
        
        # make all final functions registred
        for key, method in map_reduce_methods.iteritems():
            results[key] = method['final'](self.objects(), results[key])

        # TODO: save results


class BaseModelAggregator(BaseAggregator):
    """
    Base class for models aggregator.
    """
    
    def __init__(self, model, manager_alias="objects"):
        self._model = model
        self._manager_alias = manager_alias
        super(BaseModelAggregator, self).__init__()

    def objects(self):
        """
        Default implementation for get model objects.
        """
        return self.queryset().iterator()

    @property
    def manager(self):
        """
        Returns the apropiate manager for current model.
        """
        return getattr(self._model, self._manager_alias)

    
    def queryset(self):
        """
        Returns the default queryset. This can be reimplemented
        on a subclass for custom querysets.
        """
        return self.manager.all()
