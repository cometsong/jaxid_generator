# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0008_auto_20151203_0936'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jaxiddetail',
            old_name='sample_type',
            new_name='sample_code',
        ),
        migrations.AlterField(
            model_name='jaxiddetail',
            name='jaxid',
            field=models.CharField(max_length=6, default='JEUZ4J', verbose_name='JAX ID', help_text='A unique ID string for every sample.'),
        ),
        migrations.AlterField(
            model_name='jaxiddetail',
            name='project_code',
            field=models.ForeignKey(to='id_generate.ProjectCode'),
        ),
        migrations.AlterField(
            model_name='projectcode',
            name='project_code',
            field=models.CharField(max_length=4, verbose_name='Project Code', help_text='Project ID code (4 chars).'),
        ),
    ]
