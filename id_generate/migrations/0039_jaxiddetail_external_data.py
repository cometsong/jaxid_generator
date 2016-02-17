# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0038_auto_20160216_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='jaxiddetail',
            name='external_data',
            field=models.BooleanField(help_text='External data (not sequenced here.)', default=False, verbose_name='External data (not sequenced here.)'),
        ),
    ]
