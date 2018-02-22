# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import nutep.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nutep', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyManager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('crm_id', models.CharField(max_length=36, null=True, blank=True)),
                ('domainname', models.CharField(max_length=50, null=True, blank=True)),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('middle_name', models.CharField(max_length=30, verbose_name='middle name', blank=True)),
                ('image', models.ImageField(null=True, upload_to=nutep.models.userprofile_path, blank=True)),
                ('mobile', models.CharField(max_length=20, verbose_name='mobile', blank=True)),
                ('phone', models.CharField(max_length=20, null=True, verbose_name='phone', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email', blank=True)),
                ('skype', models.CharField(max_length=20, null=True, verbose_name='skype', blank=True)),
                ('head', models.ForeignKey(blank=True, to='nutep.Employee', null=True)),
                ('users', models.ManyToManyField(related_name='managers', through='nutep.CompanyManager', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Scope',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='crm_id',
            field=models.CharField(max_length=36, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='fullname',
            field=models.CharField(max_length=150, verbose_name='company full name', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='name',
            field=models.CharField(max_length=100, verbose_name='company name', blank=True),
        ),
        migrations.AddField(
            model_name='companymanager',
            name='employee',
            field=models.ForeignKey(related_name='membership', to='nutep.Employee'),
        ),
        migrations.AddField(
            model_name='companymanager',
            name='scope',
            field=models.ForeignKey(blank=True, to='nutep.Scope', null=True),
        ),
        migrations.AddField(
            model_name='companymanager',
            name='user',
            field=models.ForeignKey(related_name='membership', to=settings.AUTH_USER_MODEL),
        ),
    ]
