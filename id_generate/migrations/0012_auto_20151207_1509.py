# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0011_auto_20151207_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jaxiddetail',
            name='jaxid',
            field=models.CharField(default='JQ6QLN', verbose_name='JAX ID', help_text='A unique ID string for every sample.', max_length=6),
        ),
    ]
