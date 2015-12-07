# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JaxidDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('project_code', models.CharField(help_text='A unique project identifiying code (4 chars).', max_length=4, verbose_name='Project Code')),
                ('collab_id', models.TextField(help_text='Collaborator sample ID.', verbose_name='Collaborator ID')),
                ('jaxid', models.ForeignKey(to='id_generate.JaxIdMasterList')),
            ],
        ),
        migrations.CreateModel(
            name='SampleType',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('sample_code', models.CharField(help_text='Sample type identifiying code (2 chars).', max_length=2, verbose_name='Sample Type Code')),
                ('details', models.TextField(help_text='Sample type detailed name.', verbose_name='Sample name details')),
            ],
        ),
        migrations.CreateModel(
            name='SequencingType',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('sequencing_code', models.CharField(help_text='Sequence type identifiying code (1 char).', max_length=1, verbose_name='Sequencing Type Code')),
                ('details', models.TextField(help_text='Sequencing type detailed name.', verbose_name='Sequencing type details')),
            ],
        ),
        migrations.RemoveField(
            model_name='projectlinks',
            name='jaxid',
        ),
        migrations.DeleteModel(
            name='ProjectLinks',
        ),
        migrations.AddField(
            model_name='jaxiddetails',
            name='sample_type',
            field=models.ForeignKey(to='id_generate.SampleType'),
        ),
        migrations.AddField(
            model_name='jaxiddetails',
            name='sequencing_type',
            field=models.ForeignKey(to='id_generate.SequencingType'),
        ),
    ]
