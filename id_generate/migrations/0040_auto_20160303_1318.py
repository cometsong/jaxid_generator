# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0039_jaxiddetail_external_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jaxiddetail',
            name='external_data',
            field=models.BooleanField(verbose_name='External data (not sequenced here.)', help_text='External data (not sequenced here.)'),
        ),
    ]
