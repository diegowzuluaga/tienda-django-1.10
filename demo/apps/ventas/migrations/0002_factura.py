# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='factura',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('total', models.IntegerField()),
                ('fecha', models.DateField()),
                ('cliente', models.ForeignKey(to='ventas.cliente')),
                ('producto', models.ForeignKey(to='ventas.producto')),
            ],
        ),
    ]
