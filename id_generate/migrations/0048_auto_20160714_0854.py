# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0047_auto_20160707_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jaxiddetail',
            name='parent_jaxid',
            field=models.CharField(max_length=6, null=True, verbose_name='Parent JAXid', blank=True, help_text='Parent ID string or leave blank if has no parent.'),
        ),
    ]
