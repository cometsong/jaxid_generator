# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0010_auto_20151207_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jaxiddetail',
            name='jaxid',
            field=models.CharField(max_length=6, verbose_name='JAX ID', default='JXQ7KS', help_text='A unique ID string for every sample.'),
        ),
        migrations.AlterField(
            model_name='jaxidmasterlist',
            name='jaxid',
            field=models.ForeignKey(to='id_generate.JAXIdDetail', on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
