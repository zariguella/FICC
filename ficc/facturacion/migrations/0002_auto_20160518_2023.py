# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proveedores', '0001_initial'),
        ('facturacion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Factulinea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.IntegerField(default=0)),
                ('precio', models.FloatField(default=0)),
                ('importe', models.FloatField(default=0)),
                ('descuento', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='FactulineaProveedor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.IntegerField(default=0)),
                ('precio', models.FloatField(default=0)),
                ('importe', models.FloatField(default=0)),
                ('descuento', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='FactulineaProveedorTmp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.IntegerField(default=0)),
                ('precio', models.FloatField(default=0)),
                ('importe', models.FloatField(default=0)),
                ('descuento', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='FactulineaTmp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.IntegerField(default=0)),
                ('precio', models.FloatField(default=0)),
                ('importe', models.FloatField(default=0)),
                ('descuento', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField(verbose_name='fecha cobro')),
                ('estado', models.CharField(max_length=10)),
                ('total', models.FloatField(default=0)),
                ('fecha_vencimiento', models.DateTimeField(verbose_name='fecha vencimiento')),
                ('borrado', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='FacturaProveedor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField(verbose_name='fecha cobro')),
                ('estado', models.CharField(max_length=10)),
                ('total', models.FloatField(default=0)),
                ('fecha_vencimiento', models.DateTimeField(verbose_name='fecha vencimiento')),
                ('borrado', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='FacturaProveedorTmp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_vencimiento', models.DateTimeField(verbose_name='fecha creacion')),
            ],
        ),
        migrations.CreateModel(
            name='FacturaTmp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_vencimiento', models.DateTimeField(verbose_name='fecha creacion')),
            ],
        ),
        migrations.RemoveField(
            model_name='articulo',
            name='iva',
        ),
        migrations.RemoveField(
            model_name='articulo',
            name='marca',
        ),
        migrations.RemoveField(
            model_name='articulo',
            name='rubro',
        ),
        migrations.RemoveField(
            model_name='itemgrupo',
            name='articulo',
        ),
        migrations.RemoveField(
            model_name='itemgrupo',
            name='grupo',
        ),
        migrations.AlterUniqueTogether(
            name='precioporproveedor',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='precioporproveedor',
            name='articulo',
        ),
        migrations.RemoveField(
            model_name='precioporproveedor',
            name='moneda',
        ),
        migrations.RemoveField(
            model_name='precioporproveedor',
            name='proveedor',
        ),
        migrations.RemoveField(
            model_name='rubro',
            name='familia',
        ),
        migrations.DeleteModel(
            name='AlicuotaIVA',
        ),
        migrations.DeleteModel(
            name='Articulo',
        ),
        migrations.DeleteModel(
            name='Cotizacion',
        ),
        migrations.DeleteModel(
            name='Familia',
        ),
        migrations.DeleteModel(
            name='Grupo',
        ),
        migrations.DeleteModel(
            name='ItemGrupo',
        ),
        migrations.DeleteModel(
            name='Marca',
        ),
        migrations.DeleteModel(
            name='PrecioPorProveedor',
        ),
        migrations.DeleteModel(
            name='Proveedor',
        ),
        migrations.DeleteModel(
            name='Rubro',
        ),
        migrations.AddField(
            model_name='facturaproveedor',
            name='proveedor',
            field=models.ForeignKey(to='proveedores.Proveedor'),
        ),
    ]
