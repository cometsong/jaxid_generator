# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0029_auto_20151223_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jaxidmasterlist',
            name='jaxid',
            field=models.CharField(verbose_name='JAX ID', max_length=6, help_text='A unique ID string for every sample.', unique=True),
        ),
        migrations.AlterField(
            model_name='nucleicacidtype',
            name='code',
            field=models.CharField(verbose_name='Type Code', max_length=20, help_text='Nucleic acid type identifiying code.', unique=True, blank=True),
        ),
    ]
