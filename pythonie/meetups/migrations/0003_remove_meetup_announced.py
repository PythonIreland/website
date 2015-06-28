# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetups', '0002_add_meetup_sponsor_relationship'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meetup',
            name='announced',
        ),
    ]
