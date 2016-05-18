from __future__ import unicode_literals

from django.db import models
from proveedores.models import Proveedor
from facturacion.models import Factura
from formas_de_pago.models import FormaDePago

class Pago(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    forma_pago = models.ForeignKey(FormaDePago, on_delete=models.CASCADE)
    importe = models.FloatField(default=0)
    fecha = models.DateTimeField('fecha creacion')
    observaciones = models.CharField(max_length=200)
