# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-21 10:37
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reactor', '0002_auto_20170821_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventsdump',
            name='events_json',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
    ]