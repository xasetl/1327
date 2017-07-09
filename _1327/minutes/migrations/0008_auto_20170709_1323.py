# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-07-09 11:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('minutes', '0007_auto_20160927_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='minutesdocument',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='documents', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='minutesdocument',
            name='moderator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='moderations', to=settings.AUTH_USER_MODEL, verbose_name='Moderator'),
        ),
    ]
