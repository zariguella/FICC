from __future__ import unicode_literals

from django.db import models

class Formapago():
    nombre = models.CharField(max_length=50)
    borrado = models.BooleanField(default=False)
