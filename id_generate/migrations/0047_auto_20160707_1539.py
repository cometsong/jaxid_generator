# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0046_auto_20160707_1522'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseRefClass',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('code', models.CharField(max_length=1, verbose_name='Code')),
                ('details', models.TextField(verbose_name='details', help_text='details')),
            ],
        ),
        migrations.AlterField(
            model_name='jaxiddetail',
            name='sample_type',
            field=models.ForeignKey(to_field='code', blank=True, to='id_generate.SampleType'),
        ),
    ]
