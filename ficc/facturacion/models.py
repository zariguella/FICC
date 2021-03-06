from __future__ import unicode_literals

from django.db import models
from inventario.models import Articulo
from proveedores.models import Proveedor

class Factura(models.Model):
    cliente = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    fecha = models.DateTimeField('fecha cobro')
    estado = models.CharField(max_length=10)
    total = models.FloatField(default=0)
    fecha_vencimiento = models.DateTimeField('fecha vencimiento')
    borrado = models.BooleanField(default=False)

class FacturaProveedor(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha = models.DateTimeField('fecha cobro')
    estado = models.CharField(max_length=10)
    total = models.FloatField(default=0)
    fecha_vencimiento = models.DateTimeField('fecha vencimiento')
    borrado = models.BooleanField(default=False)

class Factulinea(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    precio = models.FloatField(default=0)
    importe = models.FloatField(default=0)
    descuento = models.IntegerField(default=0)

class FactulineaTmp(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    precio = models.FloatField(default=0)
    importe = models.FloatField(default=0)
    descuento = models.IntegerField(default=0)

class FactulineaProveedor(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    precio = models.FloatField(default=0)
    importe = models.FloatField(default=0)
    descuento = models.IntegerField(default=0)

class FactulineaProveedorTmp(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    precio = models.FloatField(default=0)
    importe = models.FloatField(default=0)
    descuento = models.IntegerField(default=0)


class FacturaProveedorTmp(models.Model):
    fecha_vencimiento = models.DateTimeField('fecha creacion')

class FacturaTmp(models.Model):
    fecha_vencimiento = models.DateTimeField('fecha creacion')
