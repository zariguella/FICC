from django.db import models
from django.db.models import Sum
from obispado.aportantes.models import Aportante
from obispado.plan_de_cuentas.models import CuentaNivel3
from obispado.libros_contables.models import *

TIPO_COMPROBANTE_CHOICES = (
                     ('f', 'Factura'),
                     ('r', 'Recibo')
)

# Create your models here.
class Venta(models.Model):
    fecha = models.DateField()
    aportante = models.ForeignKey(Aportante)
    numero_factura = models.CharField(max_length=15, unique=True)
    #detalle = models.ManyToManyField(CuentaNivel3, through='VentaDetalle')
    asiento = models.ForeignKey(AsientoContable, null=True)
    tipo_comprobante = models.CharField(max_length=1, choices=TIPO_COMPROBANTE_CHOICES)
    def __unicode__(self):
        return '%d' % (self.id)
    
# class VentaDetalle(models.Model):
    # venta = models.ForeignKey(Venta)
    # cuenta = models.ForeignKey(CuentaNivel3)
    # cantidad = models.IntegerField()
    # exenta = models.FloatField(null=True)

def generar_resumen_ingresos(fecha_desde, fecha_hasta):
    '''Genera la planilla de ingresos'''
    ventas = Venta.objects.filter(fecha__range=(fecha_desde, fecha_hasta)).order_by('fecha')
    resultado = []
    
    for v in ventas:
        mini_dic = {}
        mini_dic['nro_factura'] = v.numero_factura
        mini_dic['fecha'] = v.fecha
        mini_dic['tipo'] = 'Factura' # ojo
        mini_dic['id_ruc'] = v.aportante.ruc # o ruc de la organizacion
        mini_dic['nombre_aportante'] = v.aportante.nombre
        mini_dic['tipo_bien'] = 'Efectivo'
        haberes = AsientoHaberDetalle.objects.filter(asiento=v.asiento)
        mas_de_un_articulo = (len(haberes) > 1)
        total = 0
        for haber in haberes:
            total += haber.monto
            if mas_de_un_articulo:
                mini_dic['concepto'] = 'Varios' # o que se puede poner?
            else:
                mini_dic['concepto'] = haber.cuenta.nombre
            mini_dic['cantidad'] = '1' # esto no me parece bien, parece que VentaDetalle debe aparecer de nuevo
        mini_dic['total_exentas'] = total
        mini_dic['total_iva_incluido'] = total
        resultado.append(mini_dic)
    return resultado