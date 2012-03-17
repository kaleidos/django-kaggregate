import unittest
from .. import QSAggregator
from ..models import KAggregate
from .models import TestModel

class TestQSAggregator(unittest.TestCase):

    def setUp(self):
        TestModel().save()
        TestModel().save()
        TestModel().save()
        self.qsagg = QSAggregator(TestModel.objects.all())
        self.qsagg.add_aggregation(key="count", map_func=lambda x: 1, reduce_func=lambda x, y: x+y)
        self.qsagg.add_aggregation(key="sum", map_func=lambda x: x.id, reduce_func=lambda x, y: x+y)
        self.qsagg.add_aggregation(key="avg", map_func=lambda x: x.id, reduce_func=lambda x, y: x+y, final_func=lambda qs, x: x/qs.count())

    def test_run(self):
        self.qsagg.run()
        self.assertEqual(KAggregate.objects.get(key="count").value, 3)
        self.assertEqual(KAggregate.objects.get(key="sum").value, 6)
        self.assertEqual(KAggregate.objects.get(key="avg").value, 2)

if __name__ == '__main__':
        unittest.main()
