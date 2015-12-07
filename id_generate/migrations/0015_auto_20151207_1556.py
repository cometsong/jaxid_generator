# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0014_auto_20151207_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='jaxiddetail',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 12, 7, 20, 56, 2, 1776, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='jaxiddetail',
            name='jaxid',
            field=models.CharField(max_length=6, help_text='A unique ID string for every sample.', verbose_name='JAX ID', default='J804ST'),
        ),
    ]
