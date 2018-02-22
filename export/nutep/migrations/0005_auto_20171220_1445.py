# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0004_auto_20171220_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='domainname',
            field=models.CharField(max_length=50),
        ),
    ]
