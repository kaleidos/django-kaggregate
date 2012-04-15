__version__ = (0, 0, 1, "final", 0)

from .base import BaseAggregator, BaseModelAggregator
from .decorators import as_map_reduce, as_django_aggregator
from .backends import get_aggregate_value, flush_current_storage

__all__ = ['BaseAggregator', 'BaseModelAggregator', 'as_map_reduce',
    'as_django_aggregator', 'get_aggregate_value', 'flush_current_storage',]
