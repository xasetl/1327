# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-02-27 17:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

	dependencies = [
		('documents', '0006_temporarydocumenttext_hash_value'),
	]

	operations = [
		migrations.AlterField(
			model_name='temporarydocumenttext',
			name='hash_value',
			field=models.CharField(default='0', max_length=40, unique=False, verbose_name='Hash value'),
		),
	]
