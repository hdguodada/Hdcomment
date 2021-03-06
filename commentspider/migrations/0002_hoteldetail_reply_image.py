# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-28 01:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commentspider', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotelDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guest_nickname', models.CharField(max_length=100)),
                ('guest_content', models.TextField()),
                ('create_time', models.DateTimeField()),
                ('commentExt_roomNum', models.CharField(max_length=20)),
                ('commentExt_roomTypeId', models.IntegerField()),
                ('commentExt_roomTypeName', models.CharField(max_length=20)),
                ('commentExt_checkInTime', models.DateTimeField()),
                ('replys_replyId', models.IntegerField()),
                ('replys_content', models.TextField()),
                ('replys_createTime', models.DateTimeField()),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commentspider.HotelIndex')),
            ],
        ),
        migrations.CreateModel(
            name='Reply_Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guset_image', models.ImageField(upload_to='')),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commentspider.HotelDetail')),
            ],
        ),
    ]
