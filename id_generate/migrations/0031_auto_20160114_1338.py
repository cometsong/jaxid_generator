# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0030_auto_20160114_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nucleicacidtype',
            name='code',
            field=models.CharField(max_length=20, unique=True, verbose_name='Type Code', help_text='Nucleic acid type identifiying code.'),
        ),
    ]
