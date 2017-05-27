# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-26 13:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='key',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='sessionID',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('PN', 'Pending'), ('AC', 'Active')], default='PN', max_length=2),
        ),
    ]