# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formas_de_pago', '0001_initial'),
        ('cartera', '0001_initial'),
        ('facturacion', '0002_auto_20160518_2023'),
    ]

    operations = [
        migrations.AddField(
            model_name='cobro',
            name='factura',
            field=models.ForeignKey(to='facturacion.Factura'),
        ),
        migrations.AddField(
            model_name='cobro',
            name='forma_de_pago',
            field=models.ForeignKey(to='formas_de_pago.FormaDePago'),
        ),
    ]
