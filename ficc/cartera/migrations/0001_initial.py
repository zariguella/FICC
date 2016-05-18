# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aportantes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cobro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('importe', models.FloatField(default=0)),
                ('fecha', models.DateTimeField(verbose_name='fecha cobro')),
                ('observaciones', models.CharField(max_length=200)),
                ('aportante', models.ForeignKey(to='aportantes.Aportante')),
            ],
        ),
    ]
