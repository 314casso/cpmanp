# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-03 09:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0034_container_dateout'),
    ]

    operations = [
        migrations.AddField(
            model_name='container',
            name='driver',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
