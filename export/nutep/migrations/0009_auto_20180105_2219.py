# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import nutep.models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0008_employee_portal_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfoSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435', db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted', models.BooleanField(default=False, verbose_name=b'\xd0\x9f\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x82\xd0\xba\xd0\xb0 \xd1\x83\xd0\xb4\xd0\xb0\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=150, verbose_name='title')),
                ('summary', models.CharField(max_length=250, verbose_name='summary')),
                ('url', models.CharField(max_length=250, verbose_name='url')),
                ('info_source', models.ForeignKey(to='nutep.InfoSource')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='employee',
            name='image',
            field=models.ImageField(null=True, upload_to=nutep.models.employee_path, blank=True),
        ),
    ]
