# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0002_auto_20151201_0931'),
    ]

    operations = [
        migrations.CreateModel(
            name='JaxidDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('project_code', models.CharField(max_length=4, help_text='A unique project identifiying code (4 chars).', verbose_name='Project Code')),
                ('collab_id', models.TextField(help_text='Collaborator sample ID.', verbose_name='Collaborator ID')),
                ('jaxid', models.ForeignKey(to='id_generate.JaxIdMasterList')),
                ('sample_type', models.ForeignKey(to='id_generate.SampleType')),
                ('sequencing_type', models.ForeignKey(to='id_generate.SequencingType')),
            ],
        ),
        migrations.RemoveField(
            model_name='jaxiddetails',
            name='jaxid',
        ),
        migrations.RemoveField(
            model_name='jaxiddetails',
            name='sample_type',
        ),
        migrations.RemoveField(
            model_name='jaxiddetails',
            name='sequencing_type',
        ),
        migrations.DeleteModel(
            name='JaxidDetails',
        ),
    ]
