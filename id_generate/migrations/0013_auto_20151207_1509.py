# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0012_auto_20151207_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jaxiddetail',
            name='jaxid',
            field=models.CharField(verbose_name='JAX ID', max_length=6, default='JVS43C', help_text='A unique ID string for every sample.'),
        ),
    ]
