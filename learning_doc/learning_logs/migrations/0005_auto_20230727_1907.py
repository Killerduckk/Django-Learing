# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2023-07-27 11:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0004_auto_20230726_0102'),
    ]

    operations = [
        migrations.AddField(
            model_name='register_writer',
            name='avatar',
            field=models.ImageField(default='user_images/default.jpg', max_length=200, upload_to='user_images'),
        ),
        migrations.AddField(
            model_name='register_writer',
            name='email',
            field=models.CharField(default=' ', max_length=200),
        ),
        migrations.AddField(
            model_name='register_writer',
            name='instroduction',
            field=models.TextField(default='这个人很神秘，什么都没有留下'),
        ),
        migrations.AddField(
            model_name='register_writer',
            name='telephone',
            field=models.CharField(default=' ', max_length=200),
        ),
        migrations.AddField(
            model_name='writer',
            name='avatar',
            field=models.ImageField(default='user_images/default.jpg', max_length=200, upload_to='user_images'),
        ),
        migrations.AddField(
            model_name='writer',
            name='email',
            field=models.CharField(default=' ', max_length=200),
        ),
        migrations.AddField(
            model_name='writer',
            name='favorite_topics',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favorite_topics', to='learning_logs.Topic'),
        ),
        migrations.AddField(
            model_name='writer',
            name='instroduction',
            field=models.TextField(default='这个人很神秘，什么都没有留下'),
        ),
        migrations.AddField(
            model_name='writer',
            name='telephone',
            field=models.CharField(default=' ', max_length=200),
        ),
    ]
