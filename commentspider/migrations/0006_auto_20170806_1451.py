# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-06 06:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commentspider', '0005_hoteldetail_wherefrom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelindex',
            name='hotel_name',
            field=models.CharField(max_length=50),
        ),
    ]