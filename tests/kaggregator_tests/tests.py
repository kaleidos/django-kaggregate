# -*- coding: utf-8 -*-

from django.test import TestCase
import kaggregate

class TestAggregator(kaggregate.BaseAggregator):
    def objects(self):
        return [1,2,3,4,5,6,7,8,9,0]

    @kaggregate.as_map_reduce(key="count")
    def count(self):
        return {
            'map': lambda x: 1,
            'reduce': lambda x, y: x+y,
        }

    @kaggregate.as_map_reduce(key="sum")
    def sum(self):
        return {
            'map': lambda x: x,
            'reduce': lambda x, y: x+y,
            'final': lambda objects, x: x,
        }


    @kaggregate.as_map_reduce(key="average")
    def average(self):
        return {
            'map': lambda x: x,
            'reduce': lambda x, y: x+y,
            'final': lambda objects, x: x/len(list(objects)),
        }


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


class TestSimpleAggregator(TestCase):
    def setUp(self):
        kaggregate.flush_current_storage()

    def test_simple_run(self):
        agg_instance = TestAggregator()
        agg_instance.run()

        self.assertEqual(kaggregate.get_aggregate_value("count"), 10)
        self.assertEqual(kaggregate.get_aggregate_value("sum"), 45)
        self.assertEqual(kaggregate.get_aggregate_value("average"), 4)

    def test_simple_run_with_prefix(self):
        agg_instance = TestAggregator()
        agg_instance.run("foo_")

        self.assertEqual(kaggregate.get_aggregate_value("foo_count"), 10)
        self.assertEqual(kaggregate.get_aggregate_value("foo_sum"), 45)
        self.assertEqual(kaggregate.get_aggregate_value("foo_average"), 4)

        self.assertEqual(kaggregate.get_aggregate_value("average"), None)
        self.assertEqual(kaggregate.get_aggregate_value("count"), None)
        self.assertEqual(kaggregate.get_aggregate_value("sum"), None)
