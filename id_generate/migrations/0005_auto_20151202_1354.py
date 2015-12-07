# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0004_auto_20151202_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jaxidmasterlist',
            name='jaxid',
            field=models.CharField(help_text='A unique ID string for every sample.', max_length=6, verbose_name='JAX ID'),
        ),
    ]
