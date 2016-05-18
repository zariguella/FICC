from __future__ import unicode_literals

from django.db import models
from facturacion.models import Factura
from aportantes.models import Aportante
from formas_de_pago.models import FormaDePago

class Cobro(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    aportante = models.ForeignKey(Aportante, on_delete=models.CASCADE)
    forma_de_pago = models.ForeignKey(FormaDePago, on_delete=models.CASCADE)
    importe = models.FloatField(default=0)
    fecha = models.DateTimeField('fecha cobro')
    observaciones = models.CharField(max_length=200)
