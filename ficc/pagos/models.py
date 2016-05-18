from __future__ import unicode_literals

from django.db import models

class Pago():
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    forma_pago = models.ForeignKey(Factura, on_delete=models.CASCADE)
    importe = models.DoubleField(default=0)
    fecha = models.DateTimeField('fecha creacion')
    observaciones = models.CharField(max_length=200)
