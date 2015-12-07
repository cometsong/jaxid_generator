# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0003_auto_20151201_0933'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectCode',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('project_code', models.CharField(help_text='Project identifiying code (4 chars).', verbose_name='Project Code', max_length=4)),
                ('details', models.TextField(help_text='Project type detailed name.', verbose_name='Project details')),
            ],
        ),
        migrations.AlterField(
            model_name='jaxiddetail',
            name='jaxid',
            field=models.CharField(help_text='A unique ID string for every sample.', verbose_name='JAX ID', max_length=6),
        ),
        migrations.AlterField(
            model_name='jaxidmasterlist',
            name='jaxid',
            field=models.ForeignKey(to='id_generate.JAXIdDetail', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='sampletype',
            name='details',
            field=models.TextField(help_text='Sample type detailed name.', verbose_name='name details'),
        ),
        migrations.AlterField(
            model_name='sampletype',
            name='sample_code',
            field=models.CharField(help_text='Sample type identifiying code (2 chars).', verbose_name='Type Code', max_length=2),
        ),
        migrations.AlterField(
            model_name='sequencingtype',
            name='details',
            field=models.TextField(help_text='Sequencing type detailed name.', verbose_name='detailed name'),
        ),
        migrations.AlterField(
            model_name='sequencingtype',
            name='sequencing_code',
            field=models.CharField(help_text='Sequence type identifiying code (1 char).', verbose_name='Type Code', max_length=1),
        ),
    ]
