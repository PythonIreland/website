# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsors', '__first__'),
        ('meetups', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeetupSponsorRelationship',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('note', models.TextField(default='', blank=True)),
                ('meetup', models.ForeignKey(to='meetups.Meetup')),
                ('sponsor', models.ForeignKey(to='sponsors.Sponsor')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='meetup',
            name='sponsors',
            field=models.ManyToManyField(through='meetups.MeetupSponsorRelationship', null=True, blank=True, to='sponsors.Sponsor'),
            preserve_default=True,
        ),
    ]
