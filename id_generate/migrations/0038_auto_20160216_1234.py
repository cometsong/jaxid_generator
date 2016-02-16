# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0037_auto_20160202_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jaxiddetail',
            name='notes',
            field=models.TextField(help_text='Notes', blank=True, verbose_name='Notes', null=True),
        ),
        migrations.AlterField(
            model_name='jaxiddetail',
            name='nucleic_acid_type',
            field=models.ForeignKey(blank=True, to_field='code', null=True, to='id_generate.NucleicAcidType'),
        ),
        migrations.AlterField(
            model_name='jaxiddetail',
            name='sequencing_type',
            field=models.ForeignKey(blank=True, to_field='code', null=True, to='id_generate.SequencingType'),
        ),
    ]
