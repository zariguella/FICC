from __future__ import unicode_literals

from django.db import models
from proveedores.models import Proveedor
from impuestos.models import Impuesto

class Familia(models.Model):
    nombre = models.CharField(max_length=50)
    borrado = models.BooleanField(default=False)

class Articulo(models.Model):
    familia = models.ForeignKey(Familia, on_delete=models.CASCADE)
    proveedores=models.ManyToManyField(Proveedor, through='ArticuloPorProveedor')
    impuestos=models.ManyToManyField(Impuesto)
    proveedores=models.ManyToManyField(Proveedor)
    fecha=models.DateTimeField('fecha creacion')
    referencia=models.CharField(max_length=20)
    ubicacion = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    descripcion_corta = models.CharField(max_length=30)
    stock = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=0) 
    precio_compra = models.FloatField(default=0) 
    precio_almacen = models.FloatField(default=0) 
    codigobarras = models.FloatField(default=0) 
    imagen = models.FloatField(default=0) 
    borrado = models.BooleanField(default=False)

class ArticuloPorProveedor(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    precio = models.FloatField(default=0) 

class Embalaje(models.Model):    
    nombre = models.CharField(max_length=50)
    borrado = models.BooleanField(default=False)

class Ubicacion(models.Model):
    nombre = models.CharField(max_length=50)
    borrado = models.BooleanField(default=False)
