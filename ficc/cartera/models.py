from __future__ import unicode_literals

from django.db import models

class Cobro(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    aportante = models.ForeignKey(Aportante, on_delete=models.CASCADE)
    forma_de_pago = models.ForeignKey(Aportante, on_delete=models.CASCADE)
    importe = models.DoubleField(default=0)
    fecha = models.DateTimeField('fecha cobro')
    observaciones = models.CharField(max_length=200)
