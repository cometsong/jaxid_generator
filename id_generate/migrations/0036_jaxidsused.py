# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0035_auto_20160118_1152'),
    ]

    operations = [
        migrations.CreateModel(
            name='JAXidsUsed',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('jaxid', models.CharField(verbose_name='JAX ID', max_length=6, help_text='A unique ID string used in prior imports.', unique=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
