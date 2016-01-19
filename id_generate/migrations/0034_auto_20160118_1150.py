# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0033_auto_20160115_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='jaxiddetail',
            name='entered_into_lims',
            field=models.BooleanField(verbose_name='Entered into LIMS', default='', help_text='Entered into LIMS'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='jaxiddetail',
            name='notes',
            field=models.TextField(verbose_name='Notes', help_text='Notes', blank=True),
        ),
    ]
