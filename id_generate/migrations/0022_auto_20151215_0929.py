# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0021_auto_20151215_0909'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jaxiddetail',
            name='sample_code',
        ),
        migrations.AddField(
            model_name='jaxiddetail',
            name='sample_type',
            field=models.ForeignKey(to_field='code', to='id_generate.SampleType', default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='jaxiddetail',
            name='project_code',
            field=models.ForeignKey(to='id_generate.ProjectCode', to_field='code'),
        ),
        migrations.AlterField(
            model_name='jaxiddetail',
            name='sequencing_type',
            field=models.ForeignKey(to='id_generate.SequencingType', to_field='code'),
        ),
        migrations.AlterField(
            model_name='projectcode',
            name='code',
            field=models.CharField(verbose_name='Project Code', unique=True, help_text='Project ID code (4 chars).', max_length=4),
        ),
        migrations.AlterField(
            model_name='sampletype',
            name='code',
            field=models.CharField(verbose_name='Type Code', unique=True, help_text='Sample type identifiying code (2 chars).', max_length=2),
        ),
        migrations.AlterField(
            model_name='sequencingtype',
            name='code',
            field=models.CharField(verbose_name='Type Code', unique=True, help_text='Sequence type identifiying code (1 char).', max_length=1),
        ),
    ]
