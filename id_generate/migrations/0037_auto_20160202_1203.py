# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('id_generate', '0036_jaxidsused'),
    ]

    operations = [
        migrations.DeleteModel(
            name='JaxIdMasterList',
        ),
        migrations.DeleteModel(
            name='JAXidsUsed',
        ),
    ]
