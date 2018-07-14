# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20180711_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='uphone',
            field=models.CharField(default=b'', max_length=11),
        ),
    ]
