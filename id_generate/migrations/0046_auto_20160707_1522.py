# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0045_auto_20160707_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jaxiddetail',
            name='sample_type',
            field=models.ForeignKey(to='id_generate.SampleType', to_field='code'),
        ),
    ]
