# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-13 23:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0033_procedurelog_procedure'),
    ]

    operations = [
        migrations.AddField(
            model_name='container',
            name='dateout',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
    ]