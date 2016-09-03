# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0048_auto_20160714_0854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jaxiddetail',
            name='sample_type',
            field=models.ForeignKey(to_field='code', to='id_generate.SampleType'),
        ),
    ]
