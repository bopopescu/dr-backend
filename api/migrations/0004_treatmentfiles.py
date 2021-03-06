# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-06-02 13:28
from __future__ import unicode_literals

import api.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20180602_1046'),
    ]

    operations = [
        migrations.CreateModel(
            name='TreatmentFiles',
            fields=[
                ('file_key', models.AutoField(primary_key=True, serialize=False)),
                ('files', models.FileField(blank=True, null=True, upload_to=api.models.get_upload_to)),
                ('created', models.DateField(null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('treatment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Treatments')),
            ],
            options={
                'verbose_name_plural': 'TreatmentFiles',
            },
        ),
    ]
