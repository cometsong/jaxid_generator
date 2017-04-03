# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0050_auto_20160902_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jaxiddetail',
            name='parent_jaxid',
            field=models.CharField(verbose_name='Parent JAXid', max_length=6, blank=True, default='', help_text='Parent ID string or leave blank if has no parent.'),
        ),
    ]
