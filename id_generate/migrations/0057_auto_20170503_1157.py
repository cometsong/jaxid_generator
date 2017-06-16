# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-03 15:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0056_auto_20170503_1005'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectcode',
            options={'verbose_name_plural': 'Projects'},
        ),
        migrations.AlterField(
            model_name='projectcode',
            name='details',
            field=models.TextField(help_text='Project type detailed name.', verbose_name='Project Details'),
        ),
    ]