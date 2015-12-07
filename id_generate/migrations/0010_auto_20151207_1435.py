# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0009_auto_20151207_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jaxiddetail',
            name='jaxid',
            field=models.CharField(max_length=6, default='J66YMS', help_text='A unique ID string for every sample.', verbose_name='JAX ID'),
        ),
    ]
