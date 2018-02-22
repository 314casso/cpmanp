# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0005_auto_20171220_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='crm_id',
            field=models.CharField(db_index=True, max_length=36, unique=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='domainname',
            field=models.CharField(unique=True, max_length=50, db_index=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='job_title',
            field=models.CharField(max_length=30, null=True, verbose_name='job title', blank=True),
        ),
    ]
