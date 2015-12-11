# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0017_auto_20151208_0929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jaxiddetail',
            name='jaxid',
            field=models.CharField(default=None, help_text='A unique ID string for every sample.', max_length=6, verbose_name='JAX ID'),
        ),
        migrations.AlterField(
            model_name='jaxidmasterlist',
            name='jaxid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='id_generate.JAXIdDetail'),
        ),
    ]
