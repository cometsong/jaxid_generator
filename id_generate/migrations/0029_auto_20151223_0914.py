# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0028_auto_20151221_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jaxidmasterlist',
            name='jaxid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='id_generate.JAXIdDetail', to_field='jaxid'),
        ),
    ]
