from django.conf import settings

KAGGREGATE_INITIALIZATION_MODULES = getattr(settings, 'KAGGREGATE_INITIALIZATION_MODULES', [])
