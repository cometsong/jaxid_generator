# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0042_auto_20160303_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jaxiddetail',
            name='entered_into_lims',
            field=models.BooleanField(default=False, verbose_name='Entered into LIMS', help_text='Entered into LIMS'),
        ),
        migrations.AlterField(
            model_name='jaxiddetail',
            name='external_data',
            field=models.BooleanField(default=False, verbose_name='External data (not sequenced here.)', help_text='External data (not sequenced here.)'),
        ),
    ]
