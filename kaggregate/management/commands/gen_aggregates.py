from django.core.management.base import BaseCommand, CommandError

from ...register import register
from ...settings import *

for module in KAGGREGATE_INITIALIZATION_MODULES:
    __import__(module)

class Command(BaseCommand):
    args = ''
    help = 'Update the aggregated data.'
    
    def handle(self, *args, **options):
        for aggregator, prefix in register.aggregators.values():
            aggregator.run(prefix)
