# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0003_employee_job_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='job_title',
            field=models.CharField(max_length=30, null=True, verbose_name='middle name', blank=True),
        ),
    ]
