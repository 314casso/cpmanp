# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-11 19:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0021_auto_20180211_1929'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ('name',), 'verbose_name': '\u043a\u043e\u043c\u043f\u0430\u043d\u0438\u044f', 'verbose_name_plural': '\u043a\u043e\u043c\u043f\u0430\u043d\u0438\u0438'},
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='fullname',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='name',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='middle_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='middle name'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='position',
            field=models.CharField(blank=True, max_length=150, verbose_name='position'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='valid_till',
            field=models.DateField(blank=True, null=True),
        ),
    ]
