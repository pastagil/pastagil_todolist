from __future__ import unicode_literals

from django.db import models


# Task model
class Task(models.Model):
    description = models.CharField(max_length=200, blank=True, null=True, verbose_name = 'Descripción')
    complete = models.BooleanField(default=False, verbose_name = 'Completada')
    
    def __str__(self):
        return self.description
