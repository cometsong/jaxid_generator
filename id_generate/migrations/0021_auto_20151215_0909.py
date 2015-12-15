# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0020_auto_20151209_1513'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectcode',
            old_name='project_code',
            new_name='code',
        ),
        migrations.RenameField(
            model_name='sampletype',
            old_name='sample_code',
            new_name='code',
        ),
        migrations.RenameField(
            model_name='sequencingtype',
            old_name='sequencing_code',
            new_name='code',
        ),
        migrations.AlterField(
            model_name='jaxidmasterlist',
            name='jaxid',
            field=models.ForeignKey(to='id_generate.JAXIdDetail', on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
