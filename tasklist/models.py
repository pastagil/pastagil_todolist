from __future__ import unicode_literals

from django.db import models


class Task(models.Model):
    description = models.CharField(max_length=200, blank=True, null=True)
