Django Kaleidos Aggregate
=========================

Django Kaleidos Aggregate is an application to generate and store aggregated data in a easy and efficient way.

Usage
-----

Create a module that register your aggregators. For example::

    import kaggregate
    from myapp.moels import TestModel

    from django.db.models import Avg

    class ModelAggregator(kaggregate.BaseModelAggregator):
        @kaggregate.as_django_aggregator(key="average")
        def averate(self):
            return Avg("num")

        @kaggregate.as_map_reduce(key="sum")
        def sum(self):
            return {
                'map': lambda x: x.num,
                'reduce': lambda x, y: x+y,
            }

    # register aggregator
    kaggregate.register.add(
        aggregator = ModelAggregator(TestModel),
        prefix = "foo-",
    )


From the views, you can accest to generated aggregate data::

    from django.views.generic import View
    import kaaggregate

    class MyView(View):
        def get(self, request):
            total_elements = kaaggregate.get_aggregate_value("foo-sum", None)
            [...]
 
To generate the aggregated data, you need put some configuration to your settings.py and execute one command.
The first step, add ``KAGGREGATE_INITIALIZATION_MODULES`` variable with list of modules on which have defined
your aggregates. Example::

    KAGGREGATE_INITIALIZATION_MODULES = [ 'myapp.myaggregates' ]

The second and the final step, yo need generate aggregates. For this, run this command::
  
    python manage.py gen_aggregates
