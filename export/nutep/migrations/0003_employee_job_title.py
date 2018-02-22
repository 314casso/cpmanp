# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0002_auto_20171220_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='job_title',
            field=models.CharField(max_length=30, verbose_name='middle name', blank=True),
        ),
    ]
