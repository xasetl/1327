# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-03-06 16:38
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import Group
from django.db import migrations
from guardian.utils import get_anonymous_user


def add_initial_groups(apps, schema_editor):
	initial_group_names = list(filter(lambda x: 'GROUP_NAME' in x and not 'DEFAULT' in x, dir(settings)))

	for group_name in initial_group_names:
		group, created = Group.objects.get_or_create(name=getattr(settings, group_name))

		if 'ANONYMOUS' in group_name:
			get_anonymous_user().groups.add(group)
		group.save()


def reverse_add_initial_groups(apps, schema_editor):
	initial_group_names = [getattr(settings, group_name) for group_name in filter(lambda x: 'GROUP_NAME' in x, dir(settings))]

	for group in Group.objects.filter(name__in=initial_group_names):
		group.delete()


class Migration(migrations.Migration):

	dependencies = [
		('user_management', '0001_initial'),
	]

	operations = [
		migrations.RunPython(add_initial_groups, reverse_code=reverse_add_initial_groups),
	]
