import unittest
from ..aggregators import QSAggregator, QSAggregatorFunc
from ..models import KAggregate
from .models import TestModel
from django.db.models import Count, Avg, Sum
from django.core.management import call_command

class TestAggregators(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        TestModel().save()
        TestModel().save()
        TestModel().save()

    def test_qs_aggregator_run(self):
        self.qsagg = QSAggregator(TestModel.objects.all())
        self.qsagg.add_aggregation(key="count", map_func=lambda x: 1, reduce_func=lambda x, y: x+y)
        self.qsagg.add_aggregation(key="sum", map_func=lambda x: x.id, reduce_func=lambda x, y: x+y)
        self.qsagg.add_aggregation(key="avg", map_func=lambda x: x.id, reduce_func=lambda x, y: x+y, final_func=lambda qs, x: x/qs.count())
        self.qsagg.run()

        self.assertEqual(KAggregate.objects.get(key="count").value, 3)
        self.assertEqual(KAggregate.objects.get(key="sum").value, 6)
        self.assertEqual(KAggregate.objects.get(key="avg").value, 2)

    def test_qs_aggregator_func_run(self):
        self.qsagg = QSAggregatorFunc(TestModel.objects.all())
        self.qsagg.add_aggregation("count", Count('id'))
        self.qsagg.add_aggregation("sum", Sum('id'))
        self.qsagg.add_aggregation("avg", Avg('id'))
        self.qsagg.run()

        self.assertEqual(KAggregate.objects.get(key="count").value, 3)
        self.assertEqual(KAggregate.objects.get(key="sum").value, 6)
        self.assertEqual(KAggregate.objects.get(key="avg").value, 2)

if __name__ == '__main__':
        unittest.main()
