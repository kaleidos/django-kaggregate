Django Kaleidos Aggregate
=========================

Django Kaleidos Aggregate is an application to generate and store aggregated data in a easy and efficient way.

Usage
-----

Create a module that register your aggregators. For example::

  from kaggregate.register import Register
  from kaggregate.aggregators import QSAggregator
  from myapp.models import MyModel
  
  register = Register()
  
  aggregator = QSAggregator(MyModel.objects.filter(published=True))
  aggregator.add_aggregation(key="count", map_func=lambda x: 1, reduce_func=lambda x, y: x+y)
  aggregator.add_aggregation(key="sum", map_func=lambda x: x.id, reduce_func=lambda x, y: x+y)
  aggregator.add_aggregation(key="avg", map_func=lambda x: x.id, reduce_func=lambda x, y: x+y, final_func=lambda qs, x: x/qs.count())
  register.add('my-aggregator-1', aggregator)

Configure your settings.py and add the list of modules that you want to import to register the aggregators. For example::

  KAGGREGATE_INITIALIZATION_MODULES = [ 'myapp.myaggregates' ]

Then you can run the manager gen_aggregates to generate and store all the aggregated data.::

  python manage.py gen_aggregates

You can see you actual aggregates with the manager show_aggregates.::

  python manage.py show_aggregates

And you can access to the generated data directly accesing to the kaggregate.models.KAggregate model data. For example::

  from kaggregate.models import KAggregate

  print KAggregate.objects.get(key="avg").value
