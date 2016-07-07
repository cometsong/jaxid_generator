# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0044_auto_20160707_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='jaxiddetail',
            name='parent_jaxid',
            field=models.CharField(verbose_name='Parent JAXid', help_text='Parent ID string or leave blank if has no parent.', max_length=6, blank=True),
        ),
        migrations.AlterField(
            model_name='jaxiddetail',
            name='jaxid',
            field=models.CharField(help_text='A unique ID string for every sample.', unique=True, max_length=6, verbose_name='JAXid'),
        ),
    ]
