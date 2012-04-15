# -*- coding: utf-8 -*-

from django.test import TestCase
import kaggregate

class AggregatorMethodLookupsTests(TestCase):
    def test_lookups_methods(self):

        class SomeAggregator(kaggregate.BaseAggregator):
            @kaggregate.as_map_reduce(key="test_key")
            def foo_method(self):
                return {}

            @kaggregate.as_django_aggregator("other_test_key")
            def foo2_method(self):
                return None

        kaggregator_instance = SomeAggregator()
        self.assertEqual(len(kaggregator_instance.map_reduce_methods()), 1)
        self.assertEqual(len(kaggregator_instance.django_aggregators_methods()), 1)
