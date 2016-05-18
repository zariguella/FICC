# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('impuestos', '0001_initial'),
        ('proveedores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Articulo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField(verbose_name='fecha creacion')),
                ('referencia', models.CharField(max_length=20)),
                ('ubicacion', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=200)),
                ('descripcion_corta', models.CharField(max_length=30)),
                ('stock', models.IntegerField(default=0)),
                ('stock_minimo', models.IntegerField(default=0)),
                ('precio_compra', models.FloatField(default=0)),
                ('precio_almacen', models.FloatField(default=0)),
                ('codigobarras', models.FloatField(default=0)),
                ('imagen', models.FloatField(default=0)),
                ('borrado', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ArticuloPorProveedor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('precio', models.FloatField(default=0)),
                ('articulo', models.ForeignKey(to='inventario.Articulo')),
                ('proveedor', models.ForeignKey(to='proveedores.Proveedor')),
            ],
        ),
        migrations.CreateModel(
            name='Embalaje',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
                ('borrado', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Familia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
                ('borrado', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Ubicacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
                ('borrado', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='articulo',
            name='familia',
            field=models.ForeignKey(to='inventario.Familia'),
        ),
        migrations.AddField(
            model_name='articulo',
            name='impuestos',
            field=models.ManyToManyField(to='impuestos.Impuesto'),
        ),
        migrations.AddField(
            model_name='articulo',
            name='proveedores',
            field=models.ManyToManyField(to='proveedores.Proveedor'),
        ),
    ]
