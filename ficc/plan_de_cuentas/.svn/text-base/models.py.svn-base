from django.db import models

TIPO_SALDO_CHOICES = (
                     ('d', 'Debe'),
                     ('h', 'Haber')
)

TIPO_IVA_CHOICES = (
                     ('c', 'Cinco'),
                     ('d', 'Diez'),
                     ('e', 'Exenta'),
                     ('n', 'No aplicable')
)

class TipoCuenta(models.Model):
    '''Activo, Pasivo, Patrimonio_Neto, Perdidas, Ganancias, etc...'''
    # hace falta esta clase? porque se puede hacer una lista como los *CHOICES
    nombre = models.CharField(max_length=40, unique=True)
    tipo_de_saldo = models.CharField(max_length=1, choices=TIPO_SALDO_CHOICES)
    def __unicode__(self):
        return self.nombre


class CuentaNivel1(models.Model):
    '''Cuenta Nivel 1'''
    nombre = models.CharField(max_length=40)
    tipo = models.ForeignKey(TipoCuenta)
    def __unicode__(self):
        if self.tipo.tipo_de_saldo == 'd':
            columna = 'Debe - '
        elif self.tipo.tipo_de_saldo == 'h':
            columna = 'Haber - '
        return columna + str(self.tipo) + ' - ' + str(self.nombre)
    class Meta:
        unique_together = (("nombre", "tipo"),)

class CuentaNivel2(models.Model):
    nombre = models.CharField(max_length=40)
    tipo = models.ForeignKey(CuentaNivel1)
    def __unicode__(self):
        return str(self.tipo) + ' - ' + str(self.nombre)
    class Meta:
        unique_together = (("nombre", "tipo"),)


class CuentaNivel3(models.Model):
    nombre = models.CharField(max_length=40)
    tipo = models.ForeignKey(CuentaNivel2)
    tipo_de_iva = models.CharField(default='n', max_length=1, choices=TIPO_IVA_CHOICES)
    def __unicode__(self):
        return str(self.tipo) + ' - ' + str(self.nombre)
    class Meta:
        unique_together = (("nombre", "tipo"),)

