# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Meetup',
            fields=[
                ('id', models.CharField(primary_key=True, max_length=100, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('announced', models.BooleanField(default=False)),
                ('event_url', models.URLField()),
                ('time', models.DateTimeField()),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField()),
                ('rsvps', models.IntegerField(default=0)),
                ('maybe_rsvps', models.IntegerField(default=0)),
                ('waitlist_count', models.IntegerField(default=0)),
                ('status', models.CharField(max_length=255)),
                ('visibility', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['time'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MeetupUpdate',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('updated', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
