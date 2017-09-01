# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-31 19:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0005_auto_20170831_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extrainfo',
            name='designation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='holds_designation', to='user_app.Designation'),
        ),
        migrations.AlterField(
            model_name='extrainfo',
            name='sanctioning_authority',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sanctioning_auth', to='user_app.Designation'),
        ),
        migrations.AlterField(
            model_name='extrainfo',
            name='sanctioning_officer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sanctioning_officer', to='user_app.Designation'),
        ),
    ]
