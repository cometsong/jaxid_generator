# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-03 16:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0059_auto_20170503_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nucleicacidtype',
            name='code',
            field=models.CharField(help_text='Nucleic acid type identifiying code.', max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='projectcode',
            name='code',
            field=models.CharField(help_text='Project ID code (4 chars).', max_length=4, unique=True),
        ),
        migrations.AlterField(
            model_name='sampletype',
            name='code',
            field=models.CharField(help_text='Sample type identifiying code (2 chars).', max_length=2, unique=True),
        ),
        migrations.AlterField(
            model_name='sequencingtype',
            name='code',
            field=models.CharField(help_text='Sequence type identifiying code (1 char).', max_length=1, unique=True),
        ),
    ]