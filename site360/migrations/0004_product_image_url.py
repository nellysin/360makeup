# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-20 15:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site360', '0003_auto_20170720_0849'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_url',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
    ]
