# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0024_auto_20151216_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jaxiddetail',
            name='sample_type',
            field=models.ForeignKey(blank=True, to='id_generate.SampleType', to_field='code'),
        ),
        migrations.AlterField(
            model_name='jaxiddetail',
            name='sequencing_type',
            field=models.ForeignKey(blank=True, to='id_generate.SequencingType', to_field='code'),
        ),
        migrations.AlterField(
            model_name='jaxidmasterlist',
            name='jaxid',
            field=models.ForeignKey(to_field='jaxid', on_delete=django.db.models.deletion.PROTECT, to='id_generate.JAXIdDetail'),
        ),
    ]
