# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0043_auto_20160303_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jaxiddetail',
            name='external_data',
            field=models.BooleanField(default=False, verbose_name='External data', help_text='External data (not sequenced here.)'),
        ),
    ]
