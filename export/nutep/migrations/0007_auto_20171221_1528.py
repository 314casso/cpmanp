# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0006_auto_20171220_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='job_title',
            field=models.CharField(max_length=100, null=True, verbose_name='job title', blank=True),
        ),
    ]
