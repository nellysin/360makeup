# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-24 03:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('site360', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='site360.Product'),
        ),
    ]
