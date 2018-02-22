# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0010_auto_20180105_2229'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'ordering': ('-date',)},
        ),
        migrations.AlterField(
            model_name='news',
            name='date',
            field=models.DateTimeField(db_index=True),
        ),
    ]
