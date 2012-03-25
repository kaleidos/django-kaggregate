from django.core.management.base import BaseCommand, CommandError
from ...models import KAggregate

class Command(BaseCommand):
    args = ''
    help = 'Show the aggregated data.'
    
    def handle(self, *args, **options):
        for aggregate in KAggregate.objects.all():
            print "%s: %f" % (aggregate.key, aggregate.value)
