from django.db import models
from django.db.models import Sum
from obispado.plan_de_cuentas.models import *

class AsientoContableManager(models.Manager):
    '''Manager personalizado para trabajar sobre todos los registros de
    Asientos'''
    def verificar_consistencia(self):
        '''Verifica si el debe y el haber tienen el mismo monto, para que la
        partida doble funcione.
        Devuelve la lista de asientos que estan mal'''
        resultado = []
        lista_de_asientos = self.all()
        for asiento in lista_de_asientos:
            lista_monto_debes = AsientoDebeDetalle.objects.filter(asiento=asiento).aggregate(suma=Sum('monto'))
            lista_monto_haberes = AsientoHaberDetalle.objects.filter(asiento=asiento).aggregate(suma=Sum('monto'))
            if lista_monto_debes['suma'] != lista_monto_haberes['suma']:
                resultado.append(asiento)
        return resultado


class AsientoContable(models.Model):
    fecha = models.DateField()
    debe = models.ManyToManyField(CuentaNivel3, through='AsientoDebeDetalle', related_name='CuentasDebe', null=True)
    haber = models.ManyToManyField(CuentaNivel3, through='AsientoHaberDetalle', related_name='CuentasHaber', null=True)
    comentario = models.CharField(max_length=100, null=True)
    objects = AsientoContableManager()

    def __unicode__(self):
        try:
            result = str(self.fecha) + ' - #:' + str(self.id) + ' - ' + self.comentario
        except:
            result = str(self.fecha) + ' - #:' + str(self.id)
        return result


class AsientoDebeDetalle(models.Model):
    asiento = models.ForeignKey(AsientoContable)
    cuenta = models.ForeignKey(CuentaNivel3)
    monto = models.FloatField()
    # UNIQUE TOGHETER, porque no puede repetirse la cuenta en el asiento
    # class Meta:
    #     unique_together = (("asiento", "cuenta"),)

    def __unicode__(self):
        return str(self.asiento) + ' - ' + str(self.id)


class AsientoHaberDetalle(models.Model):
    asiento = models.ForeignKey(AsientoContable)
    cuenta = models.ForeignKey(CuentaNivel3)
    monto = models.FloatField()
    # UNIQUE TOGHETER, porque no puede repetirse la cuenta en el asiento
    # class Meta:
    #     unique_together = (("asiento", "cuenta"),)

    def __unicode__(self):
        return str(self.asiento) + ' - ' + str(self.id)


# funciones de consulta a la base de datos
def generar_balance(fecha_desde, fecha_hasta):
    '''Genera el balance General'''
    # TODO: Tema de las fechas, como hacer eso?
    # tal vez se podria pasar el parametro de mes, luego cuando se traen los
    # saldos de AsientoDebeDetalle y AsientoHaberDetalle filtrar por fecha,
    # usando filter (date <= fecha_que_me_paso_el_usuario)
    # aporte fantastico de fede.caceres
    # http://docs.djangoproject.com/en/1.2/ref/models/querysets/#range

    grupos_de_cuentas = TipoCuenta.objects.all()
    diccionario_balance = {}
    # Disculpame Kreitmayr por la falta de recursividad en esta parte :)
    for g in grupos_de_cuentas:
        diccionario_balance[g] = {'suma': 0}
        lista_nivel1 = CuentaNivel1.objects.filter(tipo=g)
        for n1 in lista_nivel1:
            diccionario_balance[g][n1] = {'suma': 0}
            lista_nivel2 = CuentaNivel2.objects.filter(tipo=n1)
            for n2 in lista_nivel2:
                diccionario_balance[g][n1][n2] = {'suma': 0}
                lista_nivel3 = CuentaNivel3.objects.filter(tipo=n2)
                for n3 in lista_nivel3:
                    diccionario_balance[g][n1][n2][n3] = {'suma': 0}

    # ya tenemos la lista completa de cuentas, ahora debemos calcular el saldo a
    # la fecha del balance
    # recorremos nuestro super diccionario de la manera mas ineficaz
    # TODO: como consultar esto en forma mas eficaz
    # segun fede.caceres, se podria usar esto
    # http://docs.djangoproject.com/en/1.2/topics/db/aggregation/
    for g in diccionario_balance:
        if g != 'suma':
            for n1 in diccionario_balance[g]:
                if n1 != 'suma':
                    for n2 in diccionario_balance[g][n1]:
                        if n2 != 'suma':
                            for n3 in diccionario_balance[g][n1][n2]:
                                if n3 != 'suma':
                                    saldo = 0
                                    lista_monto_debe_n3 = AsientoDebeDetalle.objects.filter(cuenta=n3)
                                    suma_monto_debe_n3 = 0
                                    for i in lista_monto_debe_n3:
                                        suma_monto_debe_n3 += i.monto
                                    lista_monto_haber_n3 = AsientoHaberDetalle.objects.filter(cuenta=n3)
                                    suma_monto_haber_n3 = 0
                                    for i in lista_monto_haber_n3:
                                        suma_monto_haber_n3 += i.monto
                                    saldo = suma_monto_debe_n3 - suma_monto_haber_n3
                                    if g.tipo_de_saldo == 'h':
                                        saldo *= -1 # por el tema del saldo, debe y haber, segun Luca Paccioli
                                    diccionario_balance[g][n1][n2][n3]['suma'] = saldo
                                    diccionario_balance[g][n1][n2]['suma'] += saldo
                            diccionario_balance[g][n1]['suma'] += diccionario_balance[g][n1][n2]['suma']
                    diccionario_balance[g]['suma'] += diccionario_balance[g][n1]['suma']
    # hasta aqui ya tenemos el balance
    return diccionario_balance


# funciones de consulta a la base de datos
def generar_balance2(fecha_desde, fecha_hasta):
    '''Genera el balance General'''
    # TODO: Tema de las fechas, como hacer eso?
    # tal vez se podria pasar el parametro de mes, luego cuando se traen los
    # saldos de AsientoDebeDetalle y AsientoHaberDetalle filtrar por fecha,
    # usando filter (date <= fecha_que_me_paso_el_usuario)
    # aporte fantastico de fede.caceres
    # http://docs.djangoproject.com/en/1.2/ref/models/querysets/#range

    grupos_de_cuentas = TipoCuenta.objects.all()
    diccionario_balance = {}
    # Disculpame Kreitmayr por la falta de recursividad en esta parte :)
    for g in grupos_de_cuentas:
        diccionario_balance[g] = {'suma': 0}
        lista_nivel1 = CuentaNivel1.objects.filter(tipo=g)
        for n1 in lista_nivel1:
            diccionario_balance[g][n1] = {'suma': 0}
            lista_nivel2 = CuentaNivel2.objects.filter(tipo=n1)
            for n2 in lista_nivel2:
                diccionario_balance[g][n1][n2] = {'suma': 0}
                lista_nivel3 = CuentaNivel3.objects.filter(tipo=n2)
                for n3 in lista_nivel3:
                    diccionario_balance[g][n1][n2][n3] = {'suma': 0}

    # ya tenemos la lista completa de cuentas, ahora debemos calcular el saldo a
    # la fecha del balance
    # recorremos nuestro super diccionario de la manera mas ineficaz
    # DONE: http://docs.djangoproject.com/en/1.2/topics/db/queries/#lookups-that-span-relationships

    for g in diccionario_balance:
        if g != 'suma':
            for n1 in diccionario_balance[g]:
                if n1 != 'suma':
                    for n2 in diccionario_balance[g][n1]:
                        if n2 != 'suma':
                            for n3 in diccionario_balance[g][n1][n2]:
                                if n3 != 'suma':
                                    saldo = 0
                                    suma_monto_debe_n3 = 0
                                    suma_monto_haber_n3 = 0

                                    lista_asientos_debe = AsientoDebeDetalle.objects.filter(asiento__fecha__range=(fecha_desde, fecha_hasta), cuenta=n3)
                                    for debe_detalle in lista_asientos_debe:
                                        suma_monto_debe_n3 += debe_detalle.monto

                                    lista_asientos_haber = AsientoHaberDetalle.objects.filter(asiento__fecha__range=(fecha_desde, fecha_hasta), cuenta=n3)
                                    for haber_detalle in lista_asientos_haber:
                                        suma_monto_haber_n3 += haber_detalle.monto

                                    saldo = suma_monto_debe_n3 - suma_monto_haber_n3
                                    if g.tipo_de_saldo == 'h':
                                        saldo *= -1 # por el tema del saldo, debe y haber, segun Luca Paccioli
                                    diccionario_balance[g][n1][n2][n3]['suma'] = saldo
                                    diccionario_balance[g][n1][n2]['suma'] += saldo
                            diccionario_balance[g][n1]['suma'] += diccionario_balance[g][n1][n2]['suma']
                    diccionario_balance[g]['suma'] += diccionario_balance[g][n1]['suma']
    # hasta aqui ya tenemos el balance
    return diccionario_balance