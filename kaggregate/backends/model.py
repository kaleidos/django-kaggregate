# -*- coding: utf-8 -*-

from .base import BaseStorageBackend
from django.db import transaction
from kaggregate.models import KAggregate

import datetime

class StorageBackend(BaseStorageBackend):
    @transaction.commit_on_success
    def save(self, key, value):
        try:
            instance = KAggregate.objects.get(pk=key)
            instance.value = value
            instance.last_update = datetime.datetime.now()
            instance.save()
        except KAggregate.DoesNotExist:
            instance = KAggregate(
                key = key,
                value = value,
                last_update = datetime.datetime.now()
            )
            instance.save()

    def current_value(self, key, default=None):
        try:
            instance = KAggregate.objects.get(pk=key)
            return instance.value
        except KAggregate.DoesNotExist:
            return default
    
    def flush(self, key):
        return KAggregate.objects.filter(pk=key).delete()

    def flushall(self):
        return KAggregate.objects.all().delete()
