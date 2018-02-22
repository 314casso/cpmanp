# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import nutep.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseError',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('code', models.CharField(db_index=True, max_length=50, null=True, blank=True)),
                ('field', models.CharField(db_index=True, max_length=50, null=True, blank=True)),
                ('message', models.TextField()),
                ('type', models.IntegerField(default=3, blank=True, db_index=True, choices=[(1, '\u041e\u0448\u0438\u0431\u043a\u0430 \u0443\u0447\u0435\u0442\u043d\u043e\u0439 \u0441\u0438\u0441\u0442\u0435\u043c\u044b'), (4, '\u041e\u0448\u0438\u0431\u043a\u0430 \u043e\u0431\u043c\u0435\u043d\u0430 \u0434\u0430\u043d\u043d\u044b\u0445'), (2, '\u041e\u0448\u0438\u0431\u043a\u0430 \u0434\u0430\u043d\u043d\u044b\u0445'), (3, '\u041e\u0448\u0438\u0431\u043a\u0430')])),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': '\u041e\u0448\u0438\u0431\u043a\u0430',
                'verbose_name_plural': '\u041e\u0448\u0438\u0431\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('file', models.FileField(null=True, upload_to=nutep.models.attachment_path, blank=True)),
                ('note', models.CharField(max_length=255, null=True, blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='HistoryMeta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('is_created', models.BooleanField(default=False)),
                ('date', models.DateTimeField(db_index=True, null=True, blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb8\xd0\xbc\xd0\xb5\xd0\xbd\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5', db_index=True)),
                ('users', models.ManyToManyField(related_name='teams', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': '\u0420\u0430\u0431\u043e\u0447\u0430\u044f \u0433\u0440\u0443\u043f\u043f\u0430',
                'verbose_name_plural': '\u0420\u0430\u0431\u043e\u0447\u0438\u0435 \u0433\u0440\u0443\u043f\u043f\u044b',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(null=True, upload_to=nutep.models.userprofile_path, blank=True)),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
