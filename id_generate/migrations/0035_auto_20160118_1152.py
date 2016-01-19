# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0034_auto_20160118_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jaxidmasterlist',
            name='jaxid',
            field=models.CharField(max_length=6, verbose_name='JAX ID', help_text='A unique ID string for every sample.', unique=True),
        ),
    ]
