# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-09 17:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ssl_monitoring', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='url',
            name='url_last_update',
        ),
    ]
