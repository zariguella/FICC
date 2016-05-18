from __future__ import unicode_literals

from django.db import models

class Impuesto(models.Model):
    nombre = models.CharField(max_length=50)
    valor = models.FloatField(default=0)
    borrado = models.BooleanField(default=False)
