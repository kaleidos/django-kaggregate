from django.core.management.base import BaseCommand, CommandError

from ...register import Register
from ...settings import *

for module in KAGGREGATE_INITIALIZATION_MODULES:
    __import__(module)

class Command(BaseCommand):
    args = ''
    help = 'Update the aggregated data.'
    
    def handle(self, *args, **options):
        register = Register()
        for aggregator in register.aggregators.values():
            aggregator.run()
