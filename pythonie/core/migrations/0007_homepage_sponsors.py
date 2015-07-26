# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsors', '0004_auto_20150726_1412'),
        ('core', '0006_homepagesponsorrelationship'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='sponsors',
            field=models.ManyToManyField(blank=True, to='sponsors.Sponsor', null=True, through='core.HomePageSponsorRelationship'),
            preserve_default=True,
        ),
    ]
