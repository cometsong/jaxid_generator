# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0015_auto_20151207_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jaxiddetail',
            name='jaxid',
            field=models.CharField(verbose_name='JAX ID', help_text='A unique ID string for every sample.', max_length=6, default='JHE5TJ'),
        ),
    ]
