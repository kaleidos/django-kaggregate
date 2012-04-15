__version__ = (0, 0, 1, "final", 0)

from .base import BaseAggregator, BaseModelAggregator
from .decorators import as_map_reduce

__all__ = ['BaseAggregator', 'BaseModelAggregator', 'as_map_reduce']
