# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-22 09:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='brands',
            old_name='brand_id',
            new_name='item_id',
        ),
        migrations.AlterField(
            model_name='brands',
            name='description',
            field=models.CharField(max_length=120),
        ),
    ]
