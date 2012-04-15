# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core import management
import kaggregate

from .models import TestModel

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


class ModelAggregator(kaggregate.BaseModelAggregator):
    @kaggregate.as_map_reduce(key="count")
    def count(self):
        return {
            'map': lambda x: 1,
            'reduce': lambda x, y: x+y,
        }

    @kaggregate.as_map_reduce(key="sum")
    def sum(self):
        return {
            'map': lambda x: x.num,
            'reduce': lambda x, y: x+y,
            'final': lambda objects, x: x,
        }

    @kaggregate.as_django_aggregator(key="average")
    def averate(self):
        from django.db.models import Count, Avg, Sum
        return Avg("num")



kaggregate.register.add(
    aggregator = TestAggregator(),
    prefix = "",
)

kaggregate.register.add(
    aggregator = TestAggregator(),
    prefix = "bar_",
)

kaggregate.register.add(
    aggregator = ModelAggregator(TestModel),
    prefix = "foo-",
)


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

    def test_simple_run_with_prefix(self):
        agg_instance = TestAggregator()
        agg_instance.run("foo_")

        self.assertEqual(kaggregate.get_aggregate_value("foo_count"), 10)
        self.assertEqual(kaggregate.get_aggregate_value("foo_sum"), 45)

        self.assertEqual(kaggregate.get_aggregate_value("average"), None)
        self.assertEqual(kaggregate.get_aggregate_value("count"), None)

class TestManagement(TestCase):
    def setUp(self):
        kaggregate.flush_current_storage()
        TestModel.objects.all().delete()

        TestModel.objects.bulk_create([
            TestModel(num=1), TestModel(num=2),
            TestModel(num=3), TestModel(num=4),
            TestModel(num=5), TestModel(num=6),
            TestModel(num=7), TestModel(num=8),
            TestModel(num=9), TestModel(num=0),
        ])

    def test_management_command(self):
        management.call_command('gen_aggregates')
        self.assertEqual(kaggregate.get_aggregate_value("count"), 10)
        self.assertEqual(kaggregate.get_aggregate_value("sum"), 45)

        self.assertEqual(kaggregate.get_aggregate_value("bar_count"), 10)
        self.assertEqual(kaggregate.get_aggregate_value("bar_sum"), 45)

        self.assertEqual(kaggregate.get_aggregate_value("foo-count"), 10)
        self.assertEqual(kaggregate.get_aggregate_value("foo-sum"), 45)
        self.assertEqual(kaggregate.get_aggregate_value("foo-average"), 4.5)


class TestModelAggregator(TestCase):
    def setUp(self):
        kaggregate.flush_current_storage()
        TestModel.objects.all().delete()

        TestModel.objects.bulk_create([
            TestModel(num=1), TestModel(num=2),
            TestModel(num=3), TestModel(num=4),
            TestModel(num=5), TestModel(num=6),
            TestModel(num=7), TestModel(num=8),
            TestModel(num=9), TestModel(num=0),
        ])

    def test_simple_run(self):
        agg_instance = ModelAggregator(TestModel)
        agg_instance.run()

        self.assertEqual(kaggregate.get_aggregate_value("count"), 10)
        self.assertEqual(kaggregate.get_aggregate_value("sum"), 45)
        self.assertEqual(kaggregate.get_aggregate_value("average"), 4.5)

    def test_simple_run_with_prefix(self):
        agg_instance = ModelAggregator(TestModel)
        agg_instance.run("foo_")

        self.assertEqual(kaggregate.get_aggregate_value("foo_count"), 10)
        self.assertEqual(kaggregate.get_aggregate_value("foo_sum"), 45)
        self.assertEqual(kaggregate.get_aggregate_value("foo_average"), 4.5)

        self.assertEqual(kaggregate.get_aggregate_value("average"), None)
        self.assertEqual(kaggregate.get_aggregate_value("count"), None)
        self.assertEqual(kaggregate.get_aggregate_value("sum"), None)

