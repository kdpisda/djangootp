# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-27 07:11
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0003_auto_20170527_0636'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='sessionID',
        ),
        migrations.AddField(
            model_name='user',
            name='uniqueKey',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]