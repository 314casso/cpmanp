# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0007_auto_20171221_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='portal_id',
            field=models.IntegerField(unique=True, null=True, blank=True),
        ),
    ]
