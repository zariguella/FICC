from django.db import models
from obispado.proveedores.models import Proveedor
from obispado.plan_de_cuentas.models import CuentaNivel3
from obispado.libros_contables.models import *

TIPO_COMPROBANTE_CHOICES = (
                     ('f', 'Factura'),
                     ('r', 'Recibo'),
                     ('a', 'Autofactura')
)

# Create your models here.
class Compra(models.Model):
    fecha = models.DateField()
    proveedor = models.ForeignKey(Proveedor)
    asiento = models.ForeignKey(AsientoContable, null=True)
    numero_comprobante = models.CharField(max_length=15)
    tipo_comprobante = models.CharField(max_length=1, choices=TIPO_COMPROBANTE_CHOICES)
    #detalle = models.ManyToManyField(CuentaNivel3, through='CompraDetalle')
    # UNIQUE TOGHETER, porque no puede repetirse la cuenta en el asiento
    class Meta:
        unique_together = (("proveedor", "numero_comprobante"),)
    
# class CompraDetalle(models.Model):
    # compra = models.ForeignKey(Compra)
    # cuenta = models.ForeignKey(CuentaNivel3)
    # gravadas5 = models.FloatField(null=True)
    # gravadas10 = models.FloatField(null=True)
    # iva5 = models.FloatField(null=True)
    # iva10 = models.FloatField(null=True)
    # exenta = models.FloatField(null=True)
    
    
def generar_resumen_egresos(fecha_desde, fecha_hasta):
    '''Genera el resumen para la planilla simplificada de egresos'''
    resultado = []
    # asi deberia quedar la planilla
    # nro_comprobante, fecha, tipo_factura_o_recibo(???? esto no esta en la BD!), identificador ruc o CI, nombre del proveedor, gravadas 10%, gravadas 5%, exentas, total iva incluido, iva10%, iva5%

    egresos = Compra.objects.filter(fecha__range=(fecha_desde, fecha_hasta)).order_by('fecha')
    for egreso in egresos:
        dic = {}
        dic['nro_comprobante'] = egreso.numero_comprobante
        dic['fecha'] = egreso.fecha
        if egreso.tipo_comprobante == 'f':
            dic['tipo_comprobante'] = 'FACTURA'
        elif egreso.tipo_comprobante == 'r':
            dic['tipo_comprobante'] = 'RECIBO'
        elif egreso.tipo_comprobante == 'a':
            dic['tipo_comprobante'] = 'AUTOFACTURA'
        dic['ruc_proveedor'] = egreso.proveedor.ruc
        dic['proveedor'] = egreso.proveedor.nombre
        # seguro que lo que viene se puede hacer de una mejor forma, con join o algo asi
        # traigo los detalles del debe
        debes = AsientoDebeDetalle.objects.filter(asiento=egreso.asiento)
        gravadas10 = 0
        gravadas5 = 0
        exentas = 0
        iva10 = 0
        iva5 = 0
        total = 0
        for i in debes:
            # suma del total
            total += i.monto
            # carga de cuentas de iva
            if i.cuenta.nombre == "IVA 10% Credito":
                iva10 += i.monto
            elif i.cuenta.nombre == "IVA 5% Credito":
                iva5 += i.monto
            # carga de gravadas y exentas
            elif i.cuenta.tipo_de_iva == 'd': # iva 10%
                gravadas10 += i.monto
            elif i.cuenta.tipo_de_iva == 'c': # iva 5%
                gravadas5 += i.monto
            elif i.cuenta.tipo_de_iva == 'e': # exenta
                exentas += i.monto
            elif i.cuenta.tipo_de_iva == 'n': # no aplicable ??? sera que puede pasar esto? por las dudas nomas
                exentas += i.monto # this is ok?
        dic['gravadas10'] = gravadas10
        dic['gravadas5'] = gravadas5
        dic['exentas'] = exentas
        dic['total'] = total
        dic['iva10'] = iva10
        dic['iva5'] = iva5
        resultado.append(dic)
    
    return resultado