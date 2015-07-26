# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsors', '0003_sponsorshiplevel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sponsorshiplevel',
            options={'ordering': ['-level']},
        ),
    ]
