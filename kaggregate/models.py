# -*- coding: utf-8 -*-
from django.db import models

class KAggregate(models.Model):
    key = models.CharField(max_length=200, db_index=True, primary_key=True)
    last_update = models.DateTimeField(null=True, default=None)
    value = models.FloatField()
