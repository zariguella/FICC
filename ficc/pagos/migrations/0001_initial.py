# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0003_auto_20160518_2023'),
        ('formas_de_pago', '0001_initial'),
        ('proveedores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('importe', models.FloatField(default=0)),
                ('fecha', models.DateTimeField(verbose_name='fecha creacion')),
                ('observaciones', models.CharField(max_length=200)),
                ('factura', models.ForeignKey(to='facturacion.Factura')),
                ('forma_pago', models.ForeignKey(to='formas_de_pago.FormaDePago')),
                ('proveedor', models.ForeignKey(to='proveedores.Proveedor')),
            ],
        ),
    ]
