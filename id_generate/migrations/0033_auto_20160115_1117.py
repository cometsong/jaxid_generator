# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0032_auto_20160114_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='jaxiddetail',
            name='notes',
            field=models.TextField(help_text='Notes', verbose_name='Notes', default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='jaxidmasterlist',
            name='jaxid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to_field='jaxid', to='id_generate.JAXIdDetail'),
        ),
    ]
