# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-05-28 07:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_user_ismobile_loggedin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='deviceId',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_supervisior',
        ),
        migrations.RemoveField(
            model_name='user',
            name='ismobile_loggedin',
        ),
        migrations.RemoveField(
            model_name='user',
            name='qrhash',
        ),
        migrations.RemoveField(
            model_name='user',
            name='qrhash_expiration',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_hostel',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_supervisor',
        ),
    ]