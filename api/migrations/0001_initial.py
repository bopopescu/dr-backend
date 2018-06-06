# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-05-31 11:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('account_key', models.AutoField(primary_key=True, serialize=False)),
                ('invoice_no', models.CharField(blank=True, max_length=300)),
                ('teeth', models.CharField(blank=True, max_length=500)),
                ('created', models.DateField(null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('total_cost', models.CharField(blank=True, max_length=500)),
                ('net_cost', models.CharField(blank=True, max_length=500)),
                ('discount', models.CharField(blank=True, max_length=500)),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Accounts',
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('appointment_key', models.AutoField(primary_key=True, serialize=False)),
                ('appointment_time', models.DateTimeField(blank=True, null=True)),
                ('created', models.DateField(null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Appointments',
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('patient_key', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=255, null=True, unique=True, verbose_name='email')),
                ('user_name', models.CharField(blank=True, max_length=30)),
                ('sex', models.CharField(blank=True, max_length=30)),
                ('age', models.CharField(blank=True, max_length=30)),
                ('phone', models.CharField(blank=True, max_length=30)),
                ('medical_history', models.CharField(blank=True, max_length=300)),
                ('address', models.CharField(blank=True, max_length=300)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('avatar', models.FileField(blank=True, null=True, upload_to='avatars/')),
                ('created', models.DateField(null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('doctor_treated', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Patient',
            },
        ),
        migrations.CreateModel(
            name='TreatmentList',
            fields=[
                ('treatment_key', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, max_length=500)),
            ],
            options={
                'verbose_name_plural': 'Treatments List',
            },
        ),
        migrations.CreateModel(
            name='Treatments',
            fields=[
                ('treatments_key', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=False)),
                ('created', models.DateField(null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Patient')),
                ('treatment_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.TreatmentList')),
            ],
            options={
                'verbose_name_plural': 'Treatments',
            },
        ),
        migrations.AddField(
            model_name='appointment',
            name='treatment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Treatments'),
        ),
        migrations.AddField(
            model_name='account',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Patient'),
        ),
        migrations.AddField(
            model_name='account',
            name='treatment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.TreatmentList'),
        ),
    ]