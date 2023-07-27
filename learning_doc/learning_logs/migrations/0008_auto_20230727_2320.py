# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2023-07-27 15:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0007_auto_20230727_2111'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favor_topics', to='learning_logs.Topic')),
            ],
        ),
        migrations.RemoveField(
            model_name='writer',
            name='favorite_topics',
        ),
        migrations.AddField(
            model_name='favorite',
            name='writer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lovers', to='learning_logs.Writer'),
        ),
    ]