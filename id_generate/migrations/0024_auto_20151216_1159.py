# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0023_auto_20151216_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jaxiddetail',
            name='jaxid',
            field=models.CharField(max_length=6, help_text='A unique ID string for every sample.', verbose_name='JAX ID', unique=True),
        ),
        migrations.AlterField(
            model_name='jaxidmasterlist',
            name='jaxid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to_field='jaxid', to='id_generate.JAXIdDetail'),
        ),
    ]
