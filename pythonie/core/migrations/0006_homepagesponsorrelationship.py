# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsors', '0004_auto_20150726_1412'),
        ('core', '0005_auto_20150726_1416'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePageSponsorRelationship',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('homepage', models.ForeignKey(to='core.HomePage')),
                ('level', models.ForeignKey(to='sponsors.SponsorshipLevel')),
                ('sponsor', models.ForeignKey(to='sponsors.Sponsor')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
