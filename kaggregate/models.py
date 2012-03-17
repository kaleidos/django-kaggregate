from django.db import models

class KAggregate(models.Model):
    key = models.SlugField(max_length=50, primary_key=True)
    value = models.FloatField()
