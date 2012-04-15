# -*- coding: utf-8 -*-

from django.test import TestCase
import kaggregate

print dir(kaggregate)

class AggregatorMethodLookupsTests(TestCase):
    def test_lookup_map_reduce_methods(self):

        class SomeAggregator(kaggregate.BaseAggregator):
            @kaggregate.as_map_reduce(key="test_key")
            def foo_method(self):
                return {}


        kaggregator_instance = SomeAggregator()
        self.assertEqual(len(kaggregator_instance.map_reduce_methods()), 1)
            
        

