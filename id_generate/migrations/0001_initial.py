# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JaxIdMasterList',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('jaxid', models.CharField(help_text='A unique ID string for every sample.', max_length=6, verbose_name='JAX ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectLinks',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('project_code', models.CharField(help_text='A unique project identifiying code (4 chars).', max_length=4, verbose_name='Project Code')),
                ('jaxid', models.ForeignKey(to='id_generate.JaxIdMasterList')),
            ],
        ),
    ]
