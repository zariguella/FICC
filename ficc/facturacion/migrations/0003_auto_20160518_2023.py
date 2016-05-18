# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
        ('facturacion', '0002_auto_20160518_2023'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='cliente',
            field=models.ForeignKey(to='inventario.Articulo'),
        ),
        migrations.AddField(
            model_name='factulineatmp',
            name='articulo',
            field=models.ForeignKey(to='inventario.Articulo'),
        ),
        migrations.AddField(
            model_name='factulineatmp',
            name='factura',
            field=models.ForeignKey(to='facturacion.Factura'),
        ),
        migrations.AddField(
            model_name='factulineaproveedortmp',
            name='articulo',
            field=models.ForeignKey(to='inventario.Articulo'),
        ),
        migrations.AddField(
            model_name='factulineaproveedortmp',
            name='factura',
            field=models.ForeignKey(to='facturacion.Factura'),
        ),
        migrations.AddField(
            model_name='factulineaproveedor',
            name='articulo',
            field=models.ForeignKey(to='inventario.Articulo'),
        ),
        migrations.AddField(
            model_name='factulineaproveedor',
            name='factura',
            field=models.ForeignKey(to='facturacion.Factura'),
        ),
        migrations.AddField(
            model_name='factulinea',
            name='articulo',
            field=models.ForeignKey(to='inventario.Articulo'),
        ),
        migrations.AddField(
            model_name='factulinea',
            name='factura',
            field=models.ForeignKey(to='facturacion.Factura'),
        ),
    ]
