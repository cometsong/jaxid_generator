# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0026_auto_20151221_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jaxidmasterlist',
            name='jaxid',
            field=models.ForeignKey(to='id_generate.JAXIdDetail', to_field='jaxid', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='nucleicacidtype',
            name='code',
            field=models.CharField(unique=True, max_length=20, verbose_name='Type Code', help_text='Nucleic acid type identifiying code.'),
        ),
    ]
