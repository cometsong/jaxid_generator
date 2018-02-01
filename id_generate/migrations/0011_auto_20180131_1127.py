# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-31 11:27
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0010_auto_20180131_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boxid',
            name='jaxid',
            field=models.CharField(max_length=6, unique=True, validators=[django.core.validators.MinLengthValidator(6)], verbose_name='Box ID'),
        ),
        migrations.AlterField(
            model_name='boxid',
            name='nucleic_acid_type',
            field=models.ForeignKey(blank=True, default='Z', null=True, on_delete=django.db.models.deletion.CASCADE, to='id_generate.NucleicAcidType', to_field='code', verbose_name='Nucleic Acid'),
        ),
        migrations.AlterField(
            model_name='boxid',
            name='project_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='id_generate.ProjectCode', to_field='code', verbose_name='Project'),
        ),
        migrations.AlterField(
            model_name='boxid',
            name='sample_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='id_generate.SampleType', to_field='code', verbose_name='Sample'),
        ),
        migrations.AlterField(
            model_name='boxid',
            name='sequencing_type',
            field=models.ForeignKey(blank=True, default='Z', null=True, on_delete=django.db.models.deletion.CASCADE, to='id_generate.SequencingType', to_field='code'),
        ),
    ]
