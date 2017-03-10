# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-09 16:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_email', models.EmailField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain_name', models.CharField(max_length=50)),
                ('domain_lead', models.EmailField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Environment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('environment_name', models.CharField(max_length=50)),
                ('is_environment_life', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=50)),
                ('service_owner', models.EmailField(max_length=100)),
                ('service_domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ssl_monitoring.Domain')),
            ],
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_fqdn', models.CharField(max_length=200)),
                ('url_current_status', models.CharField(choices=[('SHA1', 'Certificate is SHA-1 Certificate'), ('EXP', 'Certificate is Expired'), ('NR', 'URL is not Reachable'), ('VLD', 'Certificate is Valid'), ('WRN', 'Certificate is about to expire')], max_length=5)),
                ('url_last_update', models.DateTimeField(auto_now=True)),
                ('url_environment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ssl_monitoring.Environment')),
            ],
        ),
        migrations.CreateModel(
            name='UrlCheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_status', models.CharField(choices=[('SHA1', 'Certificate is SHA-1 Certificate'), ('EXP', 'Certificate is Expired'), ('NR', 'URL is not Reachable'), ('VLD', 'Certificate is Valid'), ('WRN', 'Certificate is about to expire')], max_length=5)),
                ('check_date_time', models.DateTimeField(auto_now=True)),
                ('url_reference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ssl_monitoring.Url')),
            ],
        ),
        migrations.AddField(
            model_name='environment',
            name='environment_service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ssl_monitoring.Service'),
        ),
        migrations.AddField(
            model_name='contact',
            name='contact_services',
            field=models.ManyToManyField(to='ssl_monitoring.Service'),
        ),
    ]
