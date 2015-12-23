# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0025_auto_20151221_1535'),
    ]

    operations = [
        migrations.CreateModel(
            name='NucleicAcidType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('code', models.CharField(verbose_name='Type Code', help_text='Nucleic acid type identifiying code.', max_length=2, unique=True)),
                ('details', models.TextField(verbose_name='name details', help_text='Nucleic acid type detailed name.')),
            ],
        ),
        migrations.AlterField(
            model_name='jaxidmasterlist',
            name='jaxid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='id_generate.JAXIdDetail', to_field='jaxid'),
        ),
        migrations.AddField(
            model_name='jaxiddetail',
            name='nucleic_acid_type',
            field=models.ForeignKey(to='id_generate.NucleicAcidType', to_field='code', default='Unknown', blank=True),
            preserve_default=False,
        ),
    ]
